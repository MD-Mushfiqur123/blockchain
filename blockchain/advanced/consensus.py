"""
Advanced consensus mechanism
"""
from typing import List, Dict, Any
from ..core.block import Block
from ..core.blockchain import Blockchain


class ConsensusEngine:
    """Consensus engine for block validation and chain selection"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
    
    def validate_block_consensus(self, block: Block) -> bool:
        """Validate block according to consensus rules"""
        # Check proof of work
        if not block.validate():
            return False
        
        # Check block size
        if block.size > 1000000:  # 1MB limit
            return False
        
        # Check transaction count
        if len(block.transactions) == 0 and block.index != 0:
            return False
        
        # Check coinbase transaction
        if len(block.transactions) > 0:
            coinbase = block.transactions[0]
            if not coinbase.get('is_coinbase', False):
                return False
        
        return True
    
    def select_chain(self, chains: List[List[Block]]) -> List[Block]:
        """Select longest valid chain (Nakamoto consensus)"""
        valid_chains = [chain for chain in chains if self._validate_chain(chain)]
        
        if not valid_chains:
            return []
        
        # Select chain with most work (simplified: longest chain)
        return max(valid_chains, key=len)
    
    def _validate_chain(self, chain: List[Block]) -> bool:
        """Validate entire chain"""
        for i in range(1, len(chain)):
            if chain[i].previous_hash != chain[i-1].hash:
                return False
            if not chain[i].validate():
                return False
        return True
    
    def calculate_chain_work(self, chain: List[Block]) -> int:
        """Calculate total chain work"""
        total_work = 0
        for block in chain:
            # Simplified work calculation
            work = 2 ** (256 - block.difficulty)
            total_work += work
        return total_work

