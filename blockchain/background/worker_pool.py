"""
Worker pool for parallel operations (Go-like)
"""
from typing import Callable, List, Any
from ..native.go_simulator import GoSimulator, Channel


class WorkerPool:
    """Go-like worker pool"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.work_channel = Channel()
        self.result_channel = Channel()
        self.workers = []
        self.running = False
    
    def start(self, worker_func: Callable):
        """Start worker pool"""
        self.running = True
        self.workers = GoSimulator.worker_pool(
            self.num_workers,
            self.work_channel,
            self.result_channel,
            worker_func
        )
    
    def submit(self, work: Any):
        """Submit work to pool"""
        if self.running:
            self.work_channel.send(work)
    
    def get_result(self) -> Any:
        """Get result from pool"""
        return self.result_channel.receive()
    
    def stop(self):
        """Stop worker pool"""
        self.running = False
        # Send poison pills
        for _ in range(self.num_workers):
            self.work_channel.send(None)
        self.work_channel.close()
        self.result_channel.close()
        
        # Wait for workers
        for worker in self.workers:
            worker.join(timeout=1.0)

