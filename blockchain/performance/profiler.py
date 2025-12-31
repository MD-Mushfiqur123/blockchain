"""
Performance profiling and monitoring
"""
import time
import threading
from typing import Dict, List, Any
from collections import defaultdict


class PerformanceProfiler:
    """Advanced performance profiler"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
        self.enabled = True
    
    def start_timer(self, operation: str) -> float:
        """Start timing an operation"""
        if not self.enabled:
            return 0.0
        return time.time()
    
    def end_timer(self, operation: str, start_time: float):
        """End timing and record"""
        if not self.enabled or start_time == 0.0:
            return
        
        duration = time.time() - start_time
        with self.lock:
            self.metrics[operation].append(duration)
            self.counters[operation] += 1
    
    def increment_counter(self, counter: str, value: int = 1):
        """Increment counter"""
        with self.lock:
            self.counters[counter] += value
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        with self.lock:
            stats = {}
            
            for operation, durations in self.metrics.items():
                if durations:
                    stats[operation] = {
                        'count': len(durations),
                        'total': sum(durations),
                        'average': sum(durations) / len(durations),
                        'min': min(durations),
                        'max': max(durations)
                    }
            
            for counter, value in self.counters.items():
                if counter not in stats:
                    stats[counter] = {'count': value}
            
            return stats
    
    def reset(self):
        """Reset all metrics"""
        with self.lock:
            self.metrics.clear()
            self.counters.clear()
    
    def time_operation(self, operation: str):
        """Context manager for timing operations"""
        return OperationTimer(self, operation)


class OperationTimer:
    """Context manager for timing operations"""
    
    def __init__(self, profiler: PerformanceProfiler, operation: str):
        self.profiler = profiler
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = self.profiler.start_timer(self.operation)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            self.profiler.end_timer(self.operation, self.start_time)

