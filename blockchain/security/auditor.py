"""
Blockchain audit and security checking
"""
from typing import List, Dict, Any
from ..core.blockchain import Blockchain
from ..core.block import Block


class BlockchainAuditor:
    """Advanced blockchain auditing system"""
    
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
    
    def audit_chain(self) -> Dict[str, Any]:
        """Perform comprehensive chain audit"""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        # Validate chain integrity
        if not self.blockchain.validate_chain():
            results['valid'] = False
            results['errors'].append('Chain validation failed')
        
        # Check block hashes
        for i in range(1, len(self.blockchain.chain)):
            if self.blockchain.chain[i].previous_hash != self.blockchain.chain[i-1].hash:
                results['valid'] = False
                results['errors'].append(f'Block {i} hash mismatch')
        
        # Check difficulty progression
        difficulties = [block.difficulty for block in self.blockchain.chain]
        if len(set(difficulties)) > 10:  # Too many difficulty changes
            results['warnings'].append('Unusual difficulty progression')
        
        # Check transaction consistency
        total_input = 0.0
        total_output = 0.0
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if not tx.get('is_coinbase', False):
                    for inp in tx.get('inputs', []):
                        total_input += 1  # Simplified
                    for out in tx.get('outputs', []):
                        total_output += out.get('amount', 0)
        
        # Statistics
        results['statistics'] = {
            'total_blocks': len(self.blockchain.chain),
            'total_transactions': sum(len(b.transactions) for b in self.blockchain.chain),
            'total_supply': self.blockchain.utxo_set.total_supply,
            'average_block_size': sum(b.size for b in self.blockchain.chain) / len(self.blockchain.chain) if self.blockchain.chain else 0
        }
        
        return results
    
    def check_double_spend(self) -> List[Dict[str, Any]]:
        """Check for double spending attempts"""
        spent_outputs = {}
        double_spends = []
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if not tx.get('is_coinbase', False):
                    for inp in tx.get('inputs', []):
                        prev_tx_id = inp.get('prev_tx_id', '')
                        prev_output_index = inp.get('prev_output_index', -1)
                        key = f"{prev_tx_id}:{prev_output_index}"
                        
                        if key in spent_outputs:
                            double_spends.append({
                                'tx_id': tx.get('tx_id', ''),
                                'block_index': block.index,
                                'spent_output': key,
                                'previous_spend': spent_outputs[key]
                            })
                        else:
                            spent_outputs[key] = {
                                'tx_id': tx.get('tx_id', ''),
                                'block_index': block.index
                            }
        
        return double_spends
    
    def verify_merkle_roots(self) -> List[Dict[str, Any]]:
        """Verify all Merkle roots"""
        errors = []
        
        for block in self.blockchain.chain:
            calculated_root = block._calculate_merkle_root()
            if calculated_root != block.merkle_root:
                errors.append({
                    'block_index': block.index,
                    'expected': calculated_root,
                    'actual': block.merkle_root
                })
        
        return errors

