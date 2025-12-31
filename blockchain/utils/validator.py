"""
Advanced validation utilities
"""
import re
from typing import Dict, Any, List
from ..crypto.encoding import base58_decode, bech32_decode
from ..crypto.hashing import double_sha256


class Validator:
    """Complex validation system"""
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate blockchain address"""
        if not address or len(address) < 26:
            return False
        
        # Try base58 decode
        try:
            decoded = base58_decode(address)
            if len(decoded) < 25:
                return False
            
            # Verify checksum
            payload = decoded[:-4]
            checksum = decoded[-4:]
            calculated_checksum = double_sha256(payload)[:4]
            
            return checksum == calculated_checksum
        except:
            # Try bech32
            try:
                hrp, data = bech32_decode(address)
                return hrp is not None and data is not None
            except:
                return False
    
    @staticmethod
    def validate_transaction_structure(tx: Dict[str, Any]) -> bool:
        """Validate transaction structure"""
        required_fields = ['tx_id', 'inputs', 'outputs']
        
        for field in required_fields:
            if field not in tx:
                return False
        
        # Validate inputs
        if not isinstance(tx['inputs'], list) or len(tx['inputs']) == 0:
            if not tx.get('is_coinbase', False):
                return False
        
        # Validate outputs
        if not isinstance(tx['outputs'], list) or len(tx['outputs']) == 0:
            return False
        
        # Validate amounts
        for output in tx['outputs']:
            if 'amount' not in output:
                return False
            if not isinstance(output['amount'], (int, float)):
                return False
            if output['amount'] < 0:
                return False
        
        return True
    
    @staticmethod
    def validate_block_structure(block: Dict[str, Any]) -> bool:
        """Validate block structure"""
        required_fields = ['index', 'hash', 'previous_hash', 'transactions', 'timestamp']
        
        for field in required_fields:
            if field not in block:
                return False
        
        # Validate index
        if not isinstance(block['index'], int) or block['index'] < 0:
            return False
        
        # Validate hash format
        if not isinstance(block['hash'], str) or len(block['hash']) != 64:
            return False
        
        # Validate transactions
        if not isinstance(block['transactions'], list):
            return False
        
        return True
    
    @staticmethod
    def validate_signature_format(signature: str) -> bool:
        """Validate signature format"""
        if not isinstance(signature, str):
            return False
        
        # Check hex format
        try:
            bytes.fromhex(signature)
            return len(signature) > 0
        except:
            return False

