"""
Network message types and structures
"""
from enum import Enum
from typing import Dict, Any
import json
import time


class MessageType(Enum):
    """Message types for P2P protocol"""
    BLOCK = "block"
    TRANSACTION = "transaction"
    GET_BLOCKS = "get_blocks"
    GET_BLOCK = "get_block"
    BLOCK_HASHES = "block_hashes"
    PING = "ping"
    PONG = "pong"
    VERSION = "version"
    VERACK = "verack"


class Message:
    """Network message structure"""
    
    def __init__(self, message_type: MessageType, data: Dict[str, Any]):
        self.type = message_type
        self.data = data
        self.timestamp = time.time()
        self.version = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return {
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp,
            'version': self.version
        }
    
    def to_json(self) -> str:
        """Serialize message to JSON"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Deserialize message from dictionary"""
        message_type = MessageType(data['type'])
        msg = cls(message_type, data['data'])
        msg.timestamp = data.get('timestamp', time.time())
        msg.version = data.get('version', 1)
        return msg

