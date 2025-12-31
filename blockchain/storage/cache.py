"""
Advanced caching system for blockchain data
"""
from typing import Dict, Optional, Any
from collections import OrderedDict
import time


class BlockCache:
    """LRU cache for blocks"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache: OrderedDict = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.timestamps: Dict[str, float] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        if key not in self.cache:
            return None
        
        # Check TTL
        if key in self.timestamps:
            if time.time() - self.timestamps[key] > self.ttl:
                self._remove(key)
                return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: str, value: Any):
        """Put item in cache"""
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        else:
            # Add new
            if len(self.cache) >= self.max_size:
                # Remove least recently used
                oldest_key = next(iter(self.cache))
                self._remove(oldest_key)
        
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def _remove(self, key: str):
        """Remove item from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.timestamps.clear()
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)

