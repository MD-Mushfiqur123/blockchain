"""
Metrics collection system
"""
import time
from typing import Dict, Any
from collections import deque


class MetricsCollector:
    """Collect and aggregate metrics"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.block_times = deque(maxlen=window_size)
        self.transaction_counts = deque(maxlen=window_size)
        self.block_sizes = deque(maxlen=window_size)
        self.last_block_time = None
    
    def record_block(self, block_size: int, tx_count: int):
        """Record block metrics"""
        current_time = time.time()
        
        if self.last_block_time:
            block_time = current_time - self.last_block_time
            self.block_times.append(block_time)
        
        self.last_block_time = current_time
        self.transaction_counts.append(tx_count)
        self.block_sizes.append(block_size)
    
    def get_average_block_time(self) -> float:
        """Get average block time"""
        if not self.block_times:
            return 0.0
        return sum(self.block_times) / len(self.block_times)
    
    def get_average_tx_count(self) -> float:
        """Get average transaction count per block"""
        if not self.transaction_counts:
            return 0.0
        return sum(self.transaction_counts) / len(self.transaction_counts)
    
    def get_average_block_size(self) -> float:
        """Get average block size"""
        if not self.block_sizes:
            return 0.0
        return sum(self.block_sizes) / len(self.block_sizes)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics"""
        return {
            'average_block_time': self.get_average_block_time(),
            'average_tx_count': self.get_average_tx_count(),
            'average_block_size': self.get_average_block_size(),
            'total_blocks': len(self.block_times),
            'throughput_tps': self.get_average_tx_count() / max(self.get_average_block_time(), 0.001)
        }

