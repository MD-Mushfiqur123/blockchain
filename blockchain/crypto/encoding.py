"""
Advanced encoding/decoding utilities
"""
import base64
import binascii
from typing import Union


# Base58 alphabet (Bitcoin style)
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58_encode(data: bytes) -> str:
    """Encode bytes to Base58"""
    if not data:
        return ''
    
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded
    
    # Add leading zeros
    return BASE58_ALPHABET[0] * leading_zeros + encoded


def base58_decode(encoded: str) -> bytes:
    """Decode Base58 string to bytes"""
    if not encoded:
        return b''
    
    # Count leading zeros
    leading_zeros = 0
    for char in encoded:
        if char == BASE58_ALPHABET[0]:
            leading_zeros += 1
        else:
            break
    
    # Convert from base58
    num = 0
    for char in encoded:
        num = num * 58 + BASE58_ALPHABET.index(char)
    
    # Convert to bytes
    decoded = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    
    # Add leading zeros
    return b'\x00' * leading_zeros + decoded


def bech32_encode(data: bytes, hrp: str = 'bc') -> str:
    """Bech32 encoding (simplified version)"""
    # Simplified bech32 implementation
    charset = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    
    # Convert bytes to 5-bit groups
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    
    # Pad to multiple of 5
    while len(bits) % 5 != 0:
        bits.append(0)
    
    # Convert to base32
    encoded = ''
    for i in range(0, len(bits), 5):
        value = sum(bits[i+j] * (2 ** (4-j)) for j in range(5))
        encoded += charset[value]
    
    return hrp + '1' + encoded


def bech32_decode(encoded: str) -> tuple:
    """Bech32 decoding (simplified version)"""
    # Simplified bech32 implementation
    if '1' not in encoded:
        return None, None
    
    hrp, data_part = encoded.rsplit('1', 1)
    charset = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    
    # Convert from base32
    bits = []
    for char in data_part:
        if char not in charset:
            return None, None
        value = charset.index(char)
        for i in range(5):
            bits.append((value >> (4 - i)) & 1)
    
    # Convert to bytes
    bytes_data = []
    for i in range(0, len(bits), 8):
        if i + 8 > len(bits):
            break
        byte_value = sum(bits[i+j] * (2 ** (7-j)) for j in range(8))
        bytes_data.append(byte_value)
    
    return hrp, bytes(bytes_data)


def hex_encode(data: bytes) -> str:
    """Encode bytes to hex string"""
    return binascii.hexlify(data).decode('ascii')


def hex_decode(hex_str: str) -> bytes:
    """Decode hex string to bytes"""
    return binascii.unhexlify(hex_str)

