"""
Go-like goroutine and channel simulator
Concurrent operations with channels
"""
import threading
import queue
from typing import Callable, Any, List
from collections import deque


class Channel:
    """Go-like channel implementation"""
    
    def __init__(self, buffer_size: int = 0):
        self.buffer_size = buffer_size
        self.queue = queue.Queue(maxsize=buffer_size if buffer_size > 0 else float('inf'))
        self.closed = False
        self.lock = threading.Lock()
    
    def send(self, item: Any) -> bool:
        """Send item to channel (like Go's ch <- item)"""
        if self.closed:
            return False
        try:
            self.queue.put(item, block=True, timeout=None)
            return True
        except:
            return False
    
    def receive(self) -> Any:
        """Receive item from channel (like Go's <- ch)"""
        try:
            return self.queue.get(block=True, timeout=None)
        except:
            return None
    
    def close(self):
        """Close channel"""
        with self.lock:
            self.closed = True
    
    def is_closed(self) -> bool:
        """Check if channel is closed"""
        return self.closed


class GoSimulator:
    """Go-like concurrent operations"""
    
    @staticmethod
    def goroutine(func: Callable, *args, **kwargs) -> threading.Thread:
        """Start a goroutine (lightweight thread)"""
        def wrapper():
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Goroutine error: {e}")
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        return thread
    
    @staticmethod
    def select(*channels: Channel, default: Any = None) -> tuple:
        """Go-like select statement (non-blocking channel receive)"""
        # Try to receive from any channel
        for i, ch in enumerate(channels):
            try:
                item = ch.queue.get_nowait()
                return (i, item)
            except queue.Empty:
                continue
        
        return (None, default)
    
    @staticmethod
    def worker_pool(num_workers: int, work_channel: Channel, result_channel: Channel, 
                    worker_func: Callable):
        """Go-like worker pool pattern"""
        def worker():
            while True:
                item = work_channel.receive()
                if item is None:  # Poison pill
                    break
                
                result = worker_func(item)
                result_channel.send(result)
        
        workers = []
        for _ in range(num_workers):
            w = GoSimulator.goroutine(worker)
            workers.append(w)
        
        return workers
    
    @staticmethod
    def pipeline(stages: List[Callable], input_channel: Channel) -> Channel:
        """Go-like pipeline pattern"""
        current_channel = input_channel
        
        for stage in stages:
            next_channel = Channel()
            
            def stage_worker():
                while True:
                    item = current_channel.receive()
                    if item is None:
                        next_channel.close()
                        break
                    result = stage(item)
                    next_channel.send(result)
            
            GoSimulator.goroutine(stage_worker)
            current_channel = next_channel
        
        return current_channel
    
    @staticmethod
    def fan_out(input_channel: Channel, num_workers: int, worker_func: Callable) -> List[Channel]:
        """Go-like fan-out pattern"""
        output_channels = [Channel() for _ in range(num_workers)]
        
        def distributor():
            idx = 0
            while True:
                item = input_channel.receive()
                if item is None:
                    for ch in output_channels:
                        ch.close()
                    break
                
                output_channels[idx].send(item)
                idx = (idx + 1) % num_workers
        
        GoSimulator.goroutine(distributor)
        return output_channels
    
    @staticmethod
    def fan_in(channels: List[Channel]) -> Channel:
        """Go-like fan-in pattern"""
        output_channel = Channel()
        
        def collector(ch: Channel):
            while True:
                item = ch.receive()
                if item is None:
                    break
                output_channel.send(item)
            output_channel.close()
        
        for ch in channels:
            GoSimulator.goroutine(collector, ch)
        
        return output_channel

