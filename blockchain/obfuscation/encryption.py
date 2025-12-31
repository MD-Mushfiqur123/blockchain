"""
Advanced encryption layers for obfuscation
"""
import base64
import hashlib
from typing import Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def _derive_key(password: bytes, salt: bytes = b'blockchain_salt_v2') -> bytes:
    """Derive encryption key from password"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_data(data: Union[bytes, str], password: bytes = b'default_key') -> bytes:
    """Encrypt data with multiple layers"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # First layer: Fernet encryption
    key = _derive_key(password)
    f = Fernet(key)
    encrypted = f.encrypt(data)
    
    # Second layer: XOR with hash
    hash_key = hashlib.sha256(password).digest()
    encrypted_bytes = bytearray(encrypted)
    for i in range(len(encrypted_bytes)):
        encrypted_bytes[i] ^= hash_key[i % len(hash_key)]
    
    # Third layer: Base64 encoding
    return base64.b64encode(bytes(encrypted_bytes))


def decrypt_data(encrypted_data: bytes, password: bytes = b'default_key') -> bytes:
    """Decrypt data with multiple layers"""
    # Reverse third layer: Base64 decode
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    # Reverse second layer: XOR with hash
    hash_key = hashlib.sha256(password).digest()
    decrypted_bytes = bytearray(encrypted_bytes)
    for i in range(len(decrypted_bytes)):
        decrypted_bytes[i] ^= hash_key[i % len(hash_key)]
    
    # Reverse first layer: Fernet decryption
    key = _derive_key(password)
    f = Fernet(key)
    return f.decrypt(bytes(decrypted_bytes))

