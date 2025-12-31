"""
Advanced cryptographic signature system using ECDSA
"""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import hashlib
import json
from typing import Tuple, Dict, Any


class KeyPair:
    """Advanced key pair management with multiple algorithms"""
    
    def __init__(self, private_key=None, public_key=None):
        if private_key is None:
            # Generate ECDSA key pair (secp256k1 like Bitcoin)
            self.private_key = ec.generate_private_key(
                ec.SECP256K1(),
                default_backend()
            )
            self.public_key = self.private_key.public_key()
        else:
            self.private_key = private_key
            self.public_key = public_key or private_key.public_key()
    
    def get_private_key_bytes(self) -> bytes:
        """Serialize private key"""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    def get_public_key_bytes(self) -> bytes:
        """Serialize public key"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
    
    def get_address(self) -> str:
        """Generate address from public key"""
        from .hashing import hash160
        from .encoding import base58_encode
        
        pubkey_bytes = self.get_public_key_bytes()
        hash160_bytes = hash160(pubkey_bytes)
        
        # Add version byte (0x00 for mainnet)
        versioned = b'\x00' + hash160_bytes
        
        # Add checksum
        checksum = hashlib.sha256(hashlib.sha256(versioned).digest()).digest()[:4]
        address_bytes = versioned + checksum
        
        return base58_encode(address_bytes)


def generate_keypair() -> KeyPair:
    """Generate new key pair"""
    return KeyPair()


def sign_transaction(transaction: Dict[str, Any], private_key) -> bytes:
    """Sign transaction with ECDSA"""
    # Create message to sign (transaction data)
    tx_data = json.dumps(transaction, sort_keys=True).encode('utf-8')
    
    # Hash the transaction
    message_hash = hashlib.sha256(tx_data).digest()
    
    # Sign with private key
    signature = private_key.sign(
        message_hash,
        ec.ECDSA(hashes.SHA256())
    )
    
    return signature


def verify_signature(transaction: Dict[str, Any], signature: bytes, public_key) -> bool:
    """Verify transaction signature"""
    try:
        # Recreate message hash
        tx_data = json.dumps(transaction, sort_keys=True).encode('utf-8')
        message_hash = hashlib.sha256(tx_data).digest()
        
        # Verify signature
        public_key.verify(
            signature,
            message_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False


def sign_data(data: bytes, private_key) -> bytes:
    """Sign arbitrary data"""
    message_hash = hashlib.sha256(data).digest()
    signature = private_key.sign(
        message_hash,
        ec.ECDSA(hashes.SHA256())
    )
    return signature


def verify_data(data: bytes, signature: bytes, public_key) -> bool:
    """Verify data signature"""
    try:
        message_hash = hashlib.sha256(data).digest()
        public_key.verify(
            signature,
            message_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False

