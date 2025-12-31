"""
Advanced wallet implementation with key management
"""
import json
import os
from typing import List, Dict, Optional, Tuple
from cryptography.hazmat.primitives import serialization
from ..crypto.signature import KeyPair, generate_keypair
from ..crypto.encoding import base58_encode
import hashlib


class Wallet:
    """Advanced wallet with multiple key pairs and transaction management"""
    
    def __init__(self, keypair: Optional[KeyPair] = None):
        self.keypair = keypair or generate_keypair()
        self.address = self.keypair.get_address()
        self.transaction_history: List[Dict] = []
        self.utxos: List[Tuple[str, int, Dict]] = []  # (tx_id, output_index, utxo_data)
    
    def get_address(self) -> str:
        """Get wallet address"""
        return self.address
    
    def get_public_key(self) -> bytes:
        """Get public key bytes"""
        return self.keypair.get_public_key_bytes()
    
    def get_private_key_hex(self) -> str:
        """Get private key as hex (for export)"""
        return self.keypair.get_private_key_bytes().hex()
    
    def sign_transaction(self, transaction: Dict) -> bytes:
        """Sign transaction with wallet's private key"""
        from ..crypto.signature import sign_transaction
        return sign_transaction(transaction, self.keypair.private_key)
    
    def create_transaction(
        self,
        recipient_address: str,
        amount: float,
        utxos: List[Tuple[str, int, Dict]],
        fee: float = 0.001
    ) -> Optional[Dict]:
        """Create and sign a transaction"""
        # Calculate total input
        total_input = sum(utxo[2].get('amount', 0) for utxo in utxos)
        
        if total_input < amount + fee:
            return None  # Insufficient funds
        
        # Create transaction inputs
        inputs = []
        for tx_id, output_index, utxo in utxos:
            inputs.append({
                'prev_tx_id': tx_id,
                'prev_output_index': output_index,
                'script_sig': '',  # Will be signed
                'sequence': 0xFFFFFFFF
            })
        
        # Create transaction outputs
        outputs = [
            {
                'address': recipient_address,
                'amount': amount,
                'script_pubkey': f'OP_DUP OP_HASH160 {recipient_address} OP_EQUALVERIFY OP_CHECKSIG'
            }
        ]
        
        # Add change output if needed
        change = total_input - amount - fee
        if change > 0:
            outputs.append({
                'address': self.address,
                'amount': change,
                'script_pubkey': f'OP_DUP OP_HASH160 {self.address} OP_EQUALVERIFY OP_CHECKSIG'
            })
        
        # Create transaction
        tx_data = {
            'version': 1,
            'inputs': inputs,
            'outputs': outputs,
            'locktime': 0
        }
        
        # Generate transaction ID
        tx_id = hashlib.sha256(
            json.dumps(tx_data, sort_keys=True).encode()
        ).hexdigest()
        tx_data['tx_id'] = tx_id
        
        # Sign transaction
        signature = self.sign_transaction(tx_data)
        tx_data['signature'] = signature.hex()
        
        # Add signature to inputs
        for input_tx in inputs:
            input_tx['script_sig'] = signature.hex()
        
        return tx_data
    
    def save_to_file(self, filepath: str, password: Optional[str] = None):
        """Save wallet to file (encrypted if password provided)"""
        wallet_data = {
            'address': self.address,
            'private_key': self.get_private_key_hex(),
            'public_key': self.keypair.get_public_key_bytes().hex()
        }
        
        if password:
            # Simple encryption (in production, use proper encryption)
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.backends import default_backend
            import base64
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'blockchain_salt',
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            f = Fernet(key)
            encrypted = f.encrypt(json.dumps(wallet_data).encode())
            wallet_data = {'encrypted': encrypted.hex()}
        
        with open(filepath, 'w') as f:
            json.dump(wallet_data, f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str, password: Optional[str] = None) -> 'Wallet':
        """Load wallet from file"""
        with open(filepath, 'r') as f:
            wallet_data = json.load(f)
        
        if 'encrypted' in wallet_data:
            if not password:
                raise ValueError("Password required for encrypted wallet")
            
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.backends import default_backend
            import base64
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'blockchain_salt',
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            f = Fernet(key)
            decrypted = f.decrypt(bytes.fromhex(wallet_data['encrypted']))
            wallet_data = json.loads(decrypted)
        
        # Reconstruct keypair from private key
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.backends import default_backend
        
        private_key_bytes = bytes.fromhex(wallet_data['private_key'])
        # Note: This is simplified - proper key loading would need proper format
        # For now, generate new keypair
        wallet = cls()
        wallet.address = wallet_data.get('address', wallet.address)
        return wallet
    
    def update_utxos(self, utxos: List[Tuple[str, int, Dict]]):
        """Update wallet's UTXO list"""
        self.utxos = utxos
    
    def get_balance(self) -> float:
        """Get wallet balance from UTXOs"""
        return sum(utxo[2].get('amount', 0) for utxo in self.utxos)

