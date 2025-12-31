"""
Advanced security validation
"""
from typing import Dict, Any
from ..crypto.signature import verify_signature
from ..utils.validator import Validator


class SecurityValidator:
    """Security-focused validator"""
    
    @staticmethod
    def validate_transaction_security(tx: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive transaction security validation"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check structure
        if not Validator.validate_transaction_structure(tx):
            result['valid'] = False
            result['errors'].append('Invalid transaction structure')
            return result
        
        # Check signature
        signature = tx.get('signature', '')
        if signature:
            if not Validator.validate_signature_format(signature):
                result['valid'] = False
                result['errors'].append('Invalid signature format')
        else:
            if not tx.get('is_coinbase', False):
                result['warnings'].append('Transaction missing signature')
        
        # Check amounts
        for output in tx.get('outputs', []):
            amount = output.get('amount', 0)
            if amount < 0:
                result['valid'] = False
                result['errors'].append('Negative output amount')
            if amount == 0:
                result['warnings'].append('Zero amount output')
        
        # Check addresses
        for output in tx.get('outputs', []):
            address = output.get('address', '')
            if address and not Validator.validate_address(address):
                result['warnings'].append(f'Invalid output address: {address[:16]}...')
        
        return result
    
    @staticmethod
    def validate_block_security(block: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive block security validation"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check structure
        if not Validator.validate_block_structure(block):
            result['valid'] = False
            result['errors'].append('Invalid block structure')
            return result
        
        # Check hash format
        block_hash = block.get('hash', '')
        if len(block_hash) != 64:
            result['valid'] = False
            result['errors'].append('Invalid hash length')
        
        # Check timestamp (not too far in future)
        import time
        timestamp = block.get('timestamp', 0)
        if timestamp > time.time() + 7200:  # 2 hours
            result['warnings'].append('Block timestamp in future')
        
        # Check transaction count
        transactions = block.get('transactions', [])
        if len(transactions) == 0 and block.get('index', 0) != 0:
            result['warnings'].append('Empty block (non-genesis)')
        
        return result

