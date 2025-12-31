"""
Assembly-like low-level operations
Direct memory manipulation and bit operations
"""
import struct
import ctypes
from typing import Union


class AssemblySimulator:
    """Assembly-like low-level operations"""
    
    @staticmethod
    def bit_rotate_left(value: int, count: int, bits: int = 32) -> int:
        """Assembly-like bit rotation left"""
        mask = (1 << bits) - 1
        value &= mask
        count %= bits
        return ((value << count) | (value >> (bits - count))) & mask
    
    @staticmethod
    def bit_rotate_right(value: int, count: int, bits: int = 32) -> int:
        """Assembly-like bit rotation right"""
        mask = (1 << bits) - 1
        value &= mask
        count %= bits
        return ((value >> count) | (value << (bits - count))) & mask
    
    @staticmethod
    def fast_xor(a: bytes, b: bytes) -> bytes:
        """Assembly-like fast XOR (SIMD-like)"""
        result = bytearray(len(a))
        for i in range(len(a)):
            result[i] = a[i] ^ b[i % len(b)]
        return bytes(result)
    
    @staticmethod
    def memory_copy(src: bytes, dst: bytearray, offset: int = 0):
        """Assembly-like memory copy"""
        for i in range(len(src)):
            if offset + i < len(dst):
                dst[offset + i] = src[i]
    
    @staticmethod
    def little_endian_to_int(data: bytes) -> int:
        """Assembly-like little-endian conversion"""
        result = 0
        for i, byte in enumerate(data):
            result |= byte << (i * 8)
        return result
    
    @staticmethod
    def int_to_little_endian(value: int, length: int) -> bytes:
        """Assembly-like int to little-endian"""
        result = bytearray(length)
        for i in range(length):
            result[i] = (value >> (i * 8)) & 0xFF
        return bytes(result)
    
    @staticmethod
    def fast_add_mod(a: int, b: int, mod: int) -> int:
        """Assembly-like modular addition"""
        return (a + b) % mod
    
    @staticmethod
    def fast_mul_mod(a: int, b: int, mod: int) -> int:
        """Assembly-like modular multiplication"""
        return (a * b) % mod
    
    @staticmethod
    def popcount(value: int) -> int:
        """Assembly-like population count (count set bits)"""
        count = 0
        while value:
            count += value & 1
            value >>= 1
        return count
    
    @staticmethod
    def bswap_32(value: int) -> int:
        """Assembly-like byte swap (32-bit)"""
        return struct.unpack('<I', struct.pack('>I', value & 0xFFFFFFFF))[0]
    
    @staticmethod
    def bswap_64(value: int) -> int:
        """Assembly-like byte swap (64-bit)"""
        return struct.unpack('<Q', struct.pack('>Q', value & 0xFFFFFFFFFFFFFFFF))[0]
    
    @staticmethod
    def clz(value: int, bits: int = 32) -> int:
        """Assembly-like count leading zeros"""
        if value == 0:
            return bits
        count = 0
        mask = 1 << (bits - 1)
        while mask and not (value & mask):
            count += 1
            mask >>= 1
        return count
    
    @staticmethod
    def ctz(value: int, bits: int = 32) -> int:
        """Assembly-like count trailing zeros"""
        if value == 0:
            return bits
        count = 0
        mask = 1
        while mask and not (value & mask):
            count += 1
            mask <<= 1
        return count

