"""
String obfuscation utilities
"""
import base64
import hashlib
from typing import Union


def obfuscate_string(text: str, key: str = 'blockchain') -> str:
    """Obfuscate string with multiple encoding layers"""
    # First: XOR with key hash
    key_hash = hashlib.sha256(key.encode()).digest()
    text_bytes = text.encode('utf-8')
    obfuscated = bytearray()
    
    for i, byte in enumerate(text_bytes):
        obfuscated.append(byte ^ key_hash[i % len(key_hash)])
    
    # Second: Base64 encoding
    encoded = base64.b64encode(bytes(obfuscated)).decode('ascii')
    
    # Third: Reverse and encode again
    reversed_encoded = encoded[::-1]
    final = base64.b64encode(reversed_encoded.encode()).decode('ascii')
    
    return final


def deobfuscate_string(obfuscated: str, key: str = 'blockchain') -> str:
    """Deobfuscate string"""
    # Reverse third layer
    decoded = base64.b64decode(obfuscated.encode()).decode('ascii')
    reversed_decoded = decoded[::-1]
    
    # Reverse second layer
    obfuscated_bytes = base64.b64decode(reversed_decoded.encode())
    
    # Reverse first layer
    key_hash = hashlib.sha256(key.encode()).digest()
    deobfuscated = bytearray()
    
    for i, byte in enumerate(obfuscated_bytes):
        deobfuscated.append(byte ^ key_hash[i % len(key_hash)])
    
    return bytes(deobfuscated).decode('utf-8')

