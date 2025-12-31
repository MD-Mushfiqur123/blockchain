"""
Advanced database layer for blockchain persistence
"""
import json
import os
import sqlite3
import threading
from pathlib import Path
from typing import List, Dict, Optional, Any
from ..core.block import Block
from ..core.blockchain import Blockchain


class BlockchainDatabase:
    """SQLite database for blockchain storage (thread-safe)"""
    
    def __init__(self, db_path: str = 'blockchain.db'):
        self.db_path = db_path
        self.local = threading.local()
        self.lock = threading.Lock()
        self._init_database()
    
    def _get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            # Enable check_same_thread=False for thread safety
            self.local.conn = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            self.local.conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging for better concurrency
        return self.local.conn
    
    def _init_database(self):
        """Initialize database schema"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Blocks table (using block_index instead of index - reserved keyword)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                block_index INTEGER PRIMARY KEY,
                hash TEXT UNIQUE NOT NULL,
                previous_hash TEXT NOT NULL,
                timestamp REAL NOT NULL,
                difficulty INTEGER NOT NULL,
                nonce INTEGER NOT NULL,
                merkle_root TEXT NOT NULL,
                size INTEGER NOT NULL,
                weight INTEGER NOT NULL,
                data TEXT NOT NULL
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                tx_id TEXT PRIMARY KEY,
                block_index INTEGER,
                inputs TEXT NOT NULL,
                outputs TEXT NOT NULL,
                signature TEXT,
                is_coinbase INTEGER DEFAULT 0,
                timestamp REAL NOT NULL,
                FOREIGN KEY (block_index) REFERENCES blocks(block_index)
            )
        ''')
        
        # UTXO table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utxos (
                tx_id TEXT NOT NULL,
                output_index INTEGER NOT NULL,
                address TEXT NOT NULL,
                amount REAL NOT NULL,
                script_pubkey TEXT NOT NULL,
                PRIMARY KEY (tx_id, output_index)
            )
        ''')
        
        # Address index
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_utxos_address 
            ON utxos(address)
        ''')
        
        conn.commit()
    
    def save_block(self, block: Block):
        """Save block to database (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO blocks 
                    (block_index, hash, previous_hash, timestamp, difficulty, nonce, 
                     merkle_root, size, weight, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    block.index,
                    block.hash,
                    block.previous_hash,
                    block.timestamp,
                    block.difficulty,
                    block.nonce,
                    block.merkle_root,
                    block.size,
                    block.weight,
                    block.to_json()
                ))
                
                # Save transactions
                for tx in block.transactions:
                    self._save_transaction_internal(tx, block.index, cursor)
                
                conn.commit()
            except sqlite3.IntegrityError:
                conn.rollback()
            except Exception as e:
                conn.rollback()
                raise e
    
    def _save_transaction_internal(self, tx: Dict, block_index: int, cursor):
        """Internal transaction save (within lock)"""
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO transactions
                (tx_id, block_index, inputs, outputs, signature, is_coinbase, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tx.get('tx_id', ''),
                block_index,
                json.dumps(tx.get('inputs', [])),
                json.dumps(tx.get('outputs', [])),
                tx.get('signature', ''),
                1 if tx.get('is_coinbase', False) else 0,
                tx.get('timestamp', 0)
            ))
        except sqlite3.IntegrityError:
            pass
    
    def save_transaction(self, tx: Dict, block_index: int):
        """Save transaction to database (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            try:
                self._save_transaction_internal(tx, block_index, cursor)
                conn.commit()
            except sqlite3.IntegrityError:
                conn.rollback()
    
    def load_block(self, index: int) -> Optional[Block]:
        """Load block from database (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
        cursor.execute('SELECT data FROM blocks WHERE block_index = ?', (index,))
        row = cursor.fetchone()
        
        if row:
            data = json.loads(row[0])
            return Block.from_dict(data)
        return None
    
    def load_blockchain(self) -> List[Block]:
        """Load entire blockchain from database (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
        cursor.execute('SELECT data FROM blocks ORDER BY block_index')
        rows = cursor.fetchall()
        
        blocks = []
        for row in rows:
            data = json.loads(row[0])
            blocks.append(Block.from_dict(data))
        
        return blocks
    
    def get_block_count(self) -> int:
        """Get total block count (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM blocks')
        return cursor.fetchone()[0]
    
    def get_transaction(self, tx_id: str) -> Optional[Dict]:
        """Get transaction by ID (thread-safe)"""
        with self.lock:
            conn = self._get_connection()
            cursor = conn.cursor()
        cursor.execute('''
            SELECT inputs, outputs, signature, is_coinbase, timestamp
            FROM transactions WHERE tx_id = ?
        ''', (tx_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'tx_id': tx_id,
                'inputs': json.loads(row[0]),
                'outputs': json.loads(row[1]),
                'signature': row[2],
                'is_coinbase': bool(row[3]),
                'timestamp': row[4]
            }
        return None
    
    def close(self):
        """Close database connection (thread-safe)"""
        with self.lock:
            if hasattr(self.local, 'conn') and self.local.conn:
                self.local.conn.close()
                self.local.conn = None

