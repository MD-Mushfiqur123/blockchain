"""
Advanced transaction builder with complex logic
"""
from typing import List, Dict, Optional, Tuple
import hashlib
import json
from ..crypto.signature import KeyPair


class TransactionBuilder:
    """Complex transaction builder with multiple output types"""
    
    def __init__(self, wallet):
        self.wallet = wallet
        self.inputs: List[Dict] = []
        self.outputs: List[Dict] = []
        self.fee: float = 0.001
        self.locktime: int = 0
    
    def add_input(self, prev_tx_id: str, prev_output_index: int, utxo_data: Dict):
        """Add transaction input"""
        self.inputs.append({
            'prev_tx_id': prev_tx_id,
            'prev_output_index': prev_output_index,
            'script_sig': '',
            'sequence': 0xFFFFFFFF,
            'utxo_data': utxo_data
        })
    
    def add_output(self, address: str, amount: float, script_type: str = 'P2PKH'):
        """Add transaction output with different script types"""
        if script_type == 'P2PKH':
            script_pubkey = f'OP_DUP OP_HASH160 {address} OP_EQUALVERIFY OP_CHECKSIG'
        elif script_type == 'P2SH':
            script_pubkey = f'OP_HASH160 {address} OP_EQUAL'
        else:
            script_pubkey = f'OP_RETURN {address}'
        
        self.outputs.append({
            'address': address,
            'amount': amount,
            'script_pubkey': script_pubkey,
            'script_type': script_type
        })
    
    def set_fee(self, fee: float):
        """Set transaction fee"""
        self.fee = fee
    
    def set_locktime(self, locktime: int):
        """Set transaction locktime"""
        self.locktime = locktime
    
    def build(self) -> Optional[Dict]:
        """Build and sign transaction"""
        # Calculate total input
        total_input = sum(inp['utxo_data'].get('amount', 0) for inp in self.inputs)
        
        # Calculate total output
        total_output = sum(out['amount'] for out in self.outputs)
        
        # Check if sufficient funds
        if total_input < total_output + self.fee:
            return None
        
        # Add change output if needed
        change = total_input - total_output - self.fee
        if change > 0.00001:  # Dust threshold
            self.add_output(self.wallet.get_address(), change)
        
        # Create transaction
        tx_data = {
            'version': 1,
            'inputs': [
                {
                    'prev_tx_id': inp['prev_tx_id'],
                    'prev_output_index': inp['prev_output_index'],
                    'script_sig': '',
                    'sequence': inp['sequence']
                }
                for inp in self.inputs
            ],
            'outputs': self.outputs,
            'locktime': self.locktime
        }
        
        # Generate transaction ID
        tx_id = hashlib.sha256(
            json.dumps(tx_data, sort_keys=True).encode()
        ).hexdigest()
        tx_data['tx_id'] = tx_id
        
        # Sign transaction
        signature = self.wallet.sign_transaction(tx_data)
        tx_data['signature'] = signature.hex()
        
        # Add signatures to inputs
        for i, inp in enumerate(tx_data['inputs']):
            inp['script_sig'] = signature.hex()
        
        return tx_data
    
    def reset(self):
        """Reset builder"""
        self.inputs = []
        self.outputs = []
        self.fee = 0.001
        self.locktime = 0

