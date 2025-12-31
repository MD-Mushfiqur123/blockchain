"""
Network protocol implementation
"""
import json
import struct
from typing import Optional
from .message import Message, MessageType


class Protocol:
    """P2P protocol handler"""
    
    MAGIC_BYTES = b'\xf9\xbe\xb4\xd9'  # Bitcoin magic bytes
    
    def serialize_message(self, message: Message) -> bytes:
        """Serialize message to bytes"""
        payload = message.to_json().encode('utf-8')
        
        # Create message header
        command = message.type.value.encode('utf-8').ljust(12, b'\x00')
        length = struct.pack('<I', len(payload))
        checksum = self._calculate_checksum(payload)
        
        # Combine: magic + command + length + checksum + payload
        header = self.MAGIC_BYTES + command + length + checksum
        return header + payload
    
    def parse_message(self, data: bytes) -> Optional[Message]:
        """Parse message from bytes"""
        if len(data) < 24:  # Minimum header size
            return None
        
        # Check magic bytes
        if data[:4] != self.MAGIC_BYTES:
            return None
        
        # Parse header
        command = data[4:16].rstrip(b'\x00').decode('utf-8')
        length = struct.unpack('<I', data[16:20])[0]
        checksum = data[20:24]
        
        if len(data) < 24 + length:
            return None
        
        # Extract payload
        payload = data[24:24+length]
        
        # Verify checksum
        if self._calculate_checksum(payload) != checksum:
            return None
        
        # Parse JSON
        try:
            payload_dict = json.loads(payload.decode('utf-8'))
            message_type = MessageType(payload_dict['type'])
            return Message(message_type, payload_dict['data'])
        except (json.JSONDecodeError, ValueError):
            return None
    
    def _calculate_checksum(self, data: bytes) -> bytes:
        """Calculate message checksum (double SHA256)"""
        import hashlib
        hash1 = hashlib.sha256(data).digest()
        hash2 = hashlib.sha256(hash1).digest()
        return hash2[:4]  # First 4 bytes

