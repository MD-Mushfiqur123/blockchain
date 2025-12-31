"""
Script execution engine (simplified Bitcoin script)
"""
import re
import hashlib
from typing import List, Any


class ScriptEngine:
    """Bitcoin-like script execution engine"""
    
    def __init__(self):
        self.stack: List[Any] = []
        self.alt_stack: List[Any] = []
    
    def execute(self, script: str) -> bool:
        """Execute script"""
        self.stack = []
        self.alt_stack = []
        
        # Parse script into operations
        operations = script.split()
        
        for op in operations:
            if not self._execute_operation(op):
                return False
        
        # Script is valid if stack has non-zero value
        if len(self.stack) == 0:
            return False
        
        result = self.stack[-1]
        if isinstance(result, (int, float)):
            return result != 0
        elif isinstance(result, str):
            return len(result) > 0
        
        return False
    
    def _execute_operation(self, op: str) -> bool:
        """Execute single operation"""
        # Stack operations
        if op == 'OP_DUP':
            if len(self.stack) == 0:
                return False
            self.stack.append(self.stack[-1])
        
        elif op == 'OP_HASH160':
            if len(self.stack) == 0:
                return False
            data = self.stack.pop()
            if isinstance(data, str):
                data = data.encode('utf-8')
            hash_result = hashlib.sha256(data).digest()[:20]
            self.stack.append(hash_result.hex())
        
        elif op == 'OP_EQUALVERIFY':
            if len(self.stack) < 2:
                return False
            a = self.stack.pop()
            b = self.stack.pop()
            if a != b:
                return False
        
        elif op == 'OP_CHECKSIG':
            # Simplified signature check
            if len(self.stack) < 2:
                return False
            pubkey = self.stack.pop()
            sig = self.stack.pop()
            # In real implementation, verify signature
            self.stack.append(1)  # Assume valid
        
        elif op == 'OP_GENESIS':
            self.stack.append('GENESIS')
        
        elif op == 'OP_RETURN':
            if len(self.stack) == 0:
                return False
            self.stack.pop()
            return True  # OP_RETURN marks transaction as invalid
        
        elif op.startswith('OP_'):
            # Unknown operation
            return False
        
        else:
            # Push data
            self.stack.append(op)
        
        return True

