"""
Advanced blockchain implementation with UTXO model and complex validation
"""
import json
import time
from typing import List, Dict, Optional, Set, Tuple
from collections import defaultdict
import threading
from .block import Block
from .genesis import create_genesis_block


class UTXOSet:
    """Unspent Transaction Output set - complex UTXO management"""
    
    def __init__(self):
        # Map: tx_id -> output_index -> UTXO data
        self.utxos: Dict[str, Dict[int, Dict]] = {}
        # Map: address -> set of (tx_id, output_index)
        self.address_utxos: Dict[str, Set[Tuple[str, int]]] = defaultdict(set)
        # Total supply tracking
        self.total_supply: float = 0.0
    
    def add_utxo(self, tx_id: str, output_index: int, utxo_data: Dict):
        """Add UTXO to set"""
        if tx_id not in self.utxos:
            self.utxos[tx_id] = {}
        
        self.utxos[tx_id][output_index] = utxo_data
        address = utxo_data.get('address', '')
        if address:
            self.address_utxos[address].add((tx_id, output_index))
        
        self.total_supply += utxo_data.get('amount', 0)
    
    def remove_utxo(self, tx_id: str, output_index: int):
        """Remove UTXO from set (spent)"""
        if tx_id in self.utxos and output_index in self.utxos[tx_id]:
            utxo_data = self.utxos[tx_id][output_index]
            address = utxo_data.get('address', '')
            if address:
                self.address_utxos[address].discard((tx_id, output_index))
            
            self.total_supply -= utxo_data.get('amount', 0)
            del self.utxos[tx_id][output_index]
            
            if not self.utxos[tx_id]:
                del self.utxos[tx_id]
    
    def get_utxo(self, tx_id: str, output_index: int) -> Optional[Dict]:
        """Get specific UTXO"""
        return self.utxos.get(tx_id, {}).get(output_index)
    
    def get_address_balance(self, address: str) -> float:
        """Get balance for address"""
        balance = 0.0
        for tx_id, output_index in self.address_utxos.get(address, set()):
            utxo = self.get_utxo(tx_id, output_index)
            if utxo:
                balance += utxo.get('amount', 0)
        return balance
    
    def get_utxos_for_address(self, address: str) -> List[Tuple[str, int, Dict]]:
        """Get all UTXOs for an address"""
        result = []
        for tx_id, output_index in self.address_utxos.get(address, set()):
            utxo = self.get_utxo(tx_id, output_index)
            if utxo:
                result.append((tx_id, output_index, utxo))
        return result


class Blockchain:
    """Advanced blockchain with UTXO model, difficulty adjustment, and complex validation"""
    
    def __init__(self, difficulty: int = 4, block_time_target: float = 1.0):
        self.chain: List[Block] = [create_genesis_block()]
        self.difficulty = difficulty
        self.block_time_target = block_time_target  # Target: 1 second per block
        self.utxo_set = UTXOSet()
        self.pending_transactions: List[Dict] = []
        self.mempool: Dict[str, Dict] = {}  # tx_id -> transaction
        self.lock = threading.RLock()
        
        # Difficulty adjustment parameters
        self.difficulty_adjustment_interval = 2016  # blocks
        self.last_adjustment_block = 0
        
        # Initialize UTXO set with genesis block
        self._update_utxo_set(self.chain[0])
    
    def _update_utxo_set(self, block: Block):
        """Update UTXO set based on block transactions"""
        for tx in block.transactions:
            tx_id = tx.get('tx_id', '')
            
            # Process inputs (spend UTXOs)
            for input_tx in tx.get('inputs', []):
                prev_tx_id = input_tx.get('prev_tx_id', '')
                prev_output_index = input_tx.get('prev_output_index', -1)
                if prev_tx_id and prev_output_index >= 0:
                    self.utxo_set.remove_utxo(prev_tx_id, prev_output_index)
            
            # Process outputs (create new UTXOs)
            for i, output in enumerate(tx.get('outputs', [])):
                utxo_data = {
                    'address': output.get('address', ''),
                    'amount': output.get('amount', 0),
                    'script_pubkey': output.get('script_pubkey', ''),
                    'tx_id': tx_id,
                    'output_index': i
                }
                self.utxo_set.add_utxo(tx_id, i, utxo_data)
    
    def _adjust_difficulty(self):
        """Adjust mining difficulty based on block time"""
        if len(self.chain) < self.difficulty_adjustment_interval:
            return
        
        if (len(self.chain) - self.last_adjustment_block) < self.difficulty_adjustment_interval:
            return
        
        # Calculate average block time
        start_block = self.chain[-self.difficulty_adjustment_interval]
        end_block = self.chain[-1]
        time_span = end_block.timestamp - start_block.timestamp
        expected_time = self.block_time_target * self.difficulty_adjustment_interval
        
        # Adjust difficulty
        ratio = expected_time / time_span if time_span > 0 else 1.0
        
        if ratio > 1.1:  # Blocks too slow
            self.difficulty = max(1, self.difficulty - 1)
        elif ratio < 0.9:  # Blocks too fast
            self.difficulty = min(32, self.difficulty + 1)
        
        self.last_adjustment_block = len(self.chain)
    
    def add_transaction(self, transaction: Dict) -> bool:
        """Add transaction to mempool with validation"""
        with self.lock:
            # Validate transaction
            if not self._validate_transaction(transaction):
                return False
            
            tx_id = transaction.get('tx_id', '')
            if tx_id in self.mempool:
                return False  # Already in mempool
            
            self.mempool[tx_id] = transaction
            self.pending_transactions.append(transaction)
            return True
    
    def _validate_transaction(self, tx: Dict) -> bool:
        """Complex transaction validation"""
        # Check structure
        if 'inputs' not in tx or 'outputs' not in tx:
            return False
        
        # Check inputs reference valid UTXOs
        input_sum = 0.0
        for input_tx in tx.get('inputs', []):
            prev_tx_id = input_tx.get('prev_tx_id', '')
            prev_output_index = input_tx.get('prev_output_index', -1)
            
            if prev_tx_id and prev_output_index >= 0:
                utxo = self.utxo_set.get_utxo(prev_tx_id, prev_output_index)
                if not utxo:
                    return False  # UTXO doesn't exist
                input_sum += utxo.get('amount', 0)
        
        # Check outputs
        output_sum = sum(output.get('amount', 0) for output in tx.get('outputs', []))
        
        # Check input >= output (transaction fee)
        if input_sum < output_sum:
            return False
        
        return True
    
    def create_block(self, miner_address: str = "") -> Block:
        """Create new block with transactions from mempool"""
        with self.lock:
            # Get transactions for block (limit to prevent oversized blocks)
            block_transactions = []
            max_block_size = 1000000  # 1MB limit
            
            for tx in self.pending_transactions[:]:
                tx_size = len(json.dumps(tx).encode('utf-8'))
                if len(json.dumps(block_transactions).encode('utf-8')) + tx_size > max_block_size:
                    break
                
                block_transactions.append(tx)
                self.pending_transactions.remove(tx)
            
            # Add coinbase transaction (mining reward)
            coinbase = self._create_coinbase_transaction(miner_address)
            block_transactions.insert(0, coinbase)
            
            # Create block
            previous_hash = self.chain[-1].hash
            block = Block(
                index=len(self.chain),
                transactions=block_transactions,
                previous_hash=previous_hash,
                difficulty=self.difficulty
            )
            
            return block
    
    def _create_coinbase_transaction(self, miner_address: str) -> Dict:
        """Create coinbase transaction (block reward)"""
        # Block reward decreases over time (halving every 210000 blocks)
        halving_interval = 210000
        halvings = len(self.chain) // halving_interval
        block_reward = 50.0 / (2 ** halvings)
        
        import hashlib
        import time
        tx_id = hashlib.sha256(
            f"{time.time()}{miner_address}{len(self.chain)}".encode()
        ).hexdigest()
        
        return {
            'tx_id': tx_id,
            'inputs': [],  # Coinbase has no inputs
            'outputs': [{
                'address': miner_address,
                'amount': block_reward,
                'script_pubkey': f'OP_DUP OP_HASH160 {miner_address} OP_EQUALVERIFY OP_CHECKSIG'
            }],
            'is_coinbase': True
        }
    
    def add_block(self, block: Block) -> bool:
        """Add block to chain with complex validation"""
        with self.lock:
            # Validate block
            if not block.validate():
                return False
            
            # Check previous hash
            if block.previous_hash != self.chain[-1].hash:
                return False
            
            # Check index
            if block.index != len(self.chain):
                return False
            
            # Validate all transactions in block
            for tx in block.transactions[1:]:  # Skip coinbase
                if not self._validate_transaction(tx):
                    return False
            
            # Add block
            self.chain.append(block)
            self._update_utxo_set(block)
            
            # Adjust difficulty
            self._adjust_difficulty()
            
            return True
    
    def mine_block(self, miner_address: str = "") -> Optional[Block]:
        """Mine a new block"""
        block = self.create_block(miner_address)
        
        if block.mine():
            if self.add_block(block):
                return block
        
        return None
    
    def get_balance(self, address: str) -> float:
        """Get balance for address"""
        return self.utxo_set.get_address_balance(address)
    
    def get_chain_info(self) -> Dict:
        """Get blockchain information"""
        return {
            'length': len(self.chain),
            'difficulty': self.difficulty,
            'total_supply': self.utxo_set.total_supply,
            'pending_transactions': len(self.pending_transactions),
            'last_block_hash': self.chain[-1].hash if self.chain else None,
            'chain_height': len(self.chain) - 1
        }
    
    def validate_chain(self) -> bool:
        """Validate entire blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            if not current.validate():
                return False
            
            if current.previous_hash != previous.hash:
                return False
        
        return True
    
    def to_dict(self) -> Dict:
        """Serialize blockchain to dictionary"""
        return {
            'chain': [block.to_dict() for block in self.chain],
            'difficulty': self.difficulty,
            'utxo_set_size': len(self.utxo_set.utxos),
            'pending_transactions_count': len(self.pending_transactions)
        }

