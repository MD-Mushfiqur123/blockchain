"""
Merkle proof implementation for SPV (Simplified Payment Verification)
"""
import hashlib
from typing import List, Tuple


class MerkleProof:
    """Merkle proof for transaction inclusion verification"""
    
    def __init__(self, transaction_hash: str, merkle_path: List[Tuple[str, bool]], root: str):
        self.transaction_hash = transaction_hash
        self.merkle_path = merkle_path  # List of (hash, is_left) tuples
        self.root = root
    
    def verify(self) -> bool:
        """Verify merkle proof"""
        current_hash = self.transaction_hash
        
        for sibling_hash, is_left in self.merkle_path:
            if is_left:
                # Sibling is on the left
                combined = sibling_hash + current_hash
            else:
                # Sibling is on the right
                combined = current_hash + sibling_hash
            
            current_hash = hashlib.sha256(
                hashlib.sha256(combined.encode()).digest()
            ).hexdigest()
        
        return current_hash == self.root


def verify_merkle_proof(tx_hash: str, merkle_path: List[Tuple[str, bool]], root: str) -> bool:
    """Verify merkle proof"""
    proof = MerkleProof(tx_hash, merkle_path, root)
    return proof.verify()

