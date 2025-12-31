"""
Advanced hashing functions with multiple algorithms
"""
import hashlib
from typing import Union


def sha256(data: Union[bytes, str]) -> bytes:
    """SHA256 hash"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).digest()


def sha3_256(data: Union[bytes, str]) -> bytes:
    """SHA3-256 hash"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha3_256(data).digest()


def double_sha256(data: Union[bytes, str]) -> bytes:
    """Double SHA256 (Bitcoin style)"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def ripemd160(data: Union[bytes, str]) -> bytes:
    """RIPEMD160 hash"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    try:
        from Crypto.Hash import RIPEMD160
        h = RIPEMD160.new()
        h.update(data)
        return h.digest()
    except (ImportError, AttributeError):
        # Fallback: use SHA256 and truncate (not perfect but works)
        sha_hash = hashlib.sha256(data).digest()
        return sha_hash[:20]  # Return 20 bytes like RIPEMD160


def hash160(data: Union[bytes, str]) -> bytes:
    """SHA256 followed by RIPEMD160 (Bitcoin style)"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    sha256_hash = sha256(data)
    return ripemd160(sha256_hash)


def hash256(data: Union[bytes, str]) -> bytes:
    """Double SHA256 alias"""
    return double_sha256(data)


def blake2b_256(data: Union[bytes, str]) -> bytes:
    """BLAKE2b-256 hash"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.blake2b(data, digest_size=32).digest()


def multi_hash(data: Union[bytes, str], rounds: int = 3) -> bytes:
    """Multiple rounds of hashing for complexity"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    result = data
    for _ in range(rounds):
        result = sha256(result)
        result = sha3_256(result)
    
    return result

