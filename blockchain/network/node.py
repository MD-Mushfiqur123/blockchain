"""
P2P node implementation for blockchain network
"""
import asyncio
import json
import time
from typing import List, Dict, Set, Optional
from ..core.blockchain import Blockchain
from ..core.block import Block
from .protocol import Protocol
from .message import Message, MessageType


class Node:
    """Advanced P2P node with network communication"""
    
    def __init__(self, blockchain: Blockchain, host: str = 'localhost', port: int = 8333):
        self.blockchain = blockchain
        self.host = host
        self.port = port
        self.peers: Set[tuple] = set()  # (host, port) tuples
        self.protocol = Protocol()
        self.running = False
        self.server = None
        self.known_blocks: Set[str] = set()
        self.known_transactions: Set[str] = set()
    
    def add_peer(self, host: str, port: int):
        """Add peer to network"""
        self.peers.add((host, port))
    
    def remove_peer(self, host: str, port: int):
        """Remove peer from network"""
        self.peers.discard((host, port))
    
    async def handle_connection(self, reader, writer):
        """Handle incoming connection"""
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                
                # Parse message
                message = self.protocol.parse_message(data)
                if message:
                    await self.handle_message(message, writer)
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def handle_message(self, message: Message, writer):
        """Handle received message"""
        if message.type == MessageType.BLOCK:
            block_data = message.data
            block = Block.from_dict(block_data)
            if self.blockchain.add_block(block):
                self.known_blocks.add(block.hash)
                # Broadcast to other peers
                await self.broadcast_block(block)
        
        elif message.type == MessageType.TRANSACTION:
            tx_data = message.data
            tx_id = tx_data.get('tx_id', '')
            if tx_id not in self.known_transactions:
                if self.blockchain.add_transaction(tx_data):
                    self.known_transactions.add(tx_id)
                    # Broadcast to other peers
                    await self.broadcast_transaction(tx_data)
        
        elif message.type == MessageType.GET_BLOCKS:
            # Send block hashes
            block_hashes = [block.hash for block in self.blockchain.chain]
            response = Message(MessageType.BLOCK_HASHES, {'hashes': block_hashes})
            writer.write(self.protocol.serialize_message(response))
            await writer.drain()
        
        elif message.type == MessageType.GET_BLOCK:
            block_hash = message.data.get('hash', '')
            block = next((b for b in self.blockchain.chain if b.hash == block_hash), None)
            if block:
                response = Message(MessageType.BLOCK, block.to_dict())
                writer.write(self.protocol.serialize_message(response))
                await writer.drain()
    
    async def broadcast_block(self, block: Block):
        """Broadcast block to all peers"""
        message = Message(MessageType.BLOCK, block.to_dict())
        data = self.protocol.serialize_message(message)
        
        for peer_host, peer_port in self.peers:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(peer_host, peer_port),
                    timeout=5.0
                )
                writer.write(data)
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"Failed to broadcast to {peer_host}:{peer_port}: {e}")
    
    async def broadcast_transaction(self, transaction: Dict):
        """Broadcast transaction to all peers"""
        message = Message(MessageType.TRANSACTION, transaction)
        data = self.protocol.serialize_message(message)
        
        for peer_host, peer_port in self.peers:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(peer_host, peer_port),
                    timeout=5.0
                )
                writer.write(data)
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"Failed to broadcast transaction to {peer_host}:{peer_port}: {e}")
    
    async def start_server(self):
        """Start P2P server"""
        self.server = await asyncio.start_server(
            self.handle_connection,
            self.host,
            self.port
        )
        self.running = True
        print(f"Node started on {self.host}:{self.port}")
        
        async with self.server:
            await self.server.serve_forever()
    
    async def connect_to_peer(self, host: str, port: int):
        """Connect to peer node"""
        try:
            reader, writer = await asyncio.open_connection(host, port)
            
            # Request block hashes
            message = Message(MessageType.GET_BLOCKS, {})
            writer.write(self.protocol.serialize_message(message))
            await writer.drain()
            
            # Read response
            data = await reader.read(4096)
            response = self.protocol.parse_message(data)
            
            if response and response.type == MessageType.BLOCK_HASHES:
                peer_hashes = response.data.get('hashes', [])
                # Sync blocks if needed
                await self.sync_blocks(peer_hashes, reader, writer)
            
            writer.close()
            await writer.wait_closed()
            self.add_peer(host, port)
        except Exception as e:
            print(f"Failed to connect to {host}:{port}: {e}")
    
    async def sync_blocks(self, peer_hashes: List[str], reader, writer):
        """Sync blocks with peer"""
        our_hashes = [block.hash for block in self.blockchain.chain]
        
        # Find missing blocks
        for i, peer_hash in enumerate(peer_hashes):
            if i < len(our_hashes) and our_hashes[i] == peer_hash:
                continue
            
            # Request block
            message = Message(MessageType.GET_BLOCK, {'hash': peer_hash})
            writer.write(self.protocol.serialize_message(message))
            await writer.drain()
            
            # Read block
            data = await reader.read(8192)
            block_message = self.protocol.parse_message(data)
            
            if block_message and block_message.type == MessageType.BLOCK:
                block = Block.from_dict(block_message.data)
                self.blockchain.add_block(block)
    
    def stop(self):
        """Stop node"""
        self.running = False
        if self.server:
            self.server.close()

