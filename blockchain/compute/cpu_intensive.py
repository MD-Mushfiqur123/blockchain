"""
CPU-intensive operations requiring maximum processing power
"""
import multiprocessing
import threading
import time
import hashlib
import math
from typing import List
import numpy as np


class CPUIntensive:
    """CPU-intensive operations"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.running = False
        self.workers = []
    
    def heavy_cryptographic_work(self, data: bytes, rounds: int = 1000000) -> bytes:
        """Heavy cryptographic operations"""
        result = data
        
        for i in range(rounds):
            # Multiple hash operations
            result = hashlib.sha256(result).digest()
            result = hashlib.sha3_256(result).digest()
            result = hashlib.blake2b(result, digest_size=32).digest()
            
            # Bit manipulation
            result = bytes([b ^ (i % 256) for b in result])
            result = bytes([(b + i) % 256 for b in result])
        
        return result
    
    def parallel_hashing(self, data_list: List[bytes], num_workers: int = None) -> List[bytes]:
        """Parallel hashing using all CPU cores"""
        if num_workers is None:
            num_workers = self.max_workers
        
        def hash_worker(data_chunk):
            results = []
            for d in data_chunk:
                # Heavy hashing
                hash_result = self.heavy_cryptographic_work(d, rounds=10000)
                results.append(hash_result)
            return results
        
        # Split work
        chunk_size = max(1, len(data_list) // num_workers)
        chunks = [data_list[i:i+chunk_size] for i in range(0, len(data_list), chunk_size)]
        
        # Use multiprocessing for true parallelism
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.map(hash_worker, chunks)
        
        # Flatten results
        return [item for sublist in results for item in sublist]
    
    def heavy_mathematical_computation(self, iterations: int = 1000000):
        """Heavy mathematical computations"""
        result = 0.0
        
        for i in range(iterations):
            # Complex mathematical operations
            x = math.sin(i) * math.cos(i * 2)
            y = math.sqrt(abs(x)) * math.log(abs(x) + 1)
            z = math.pow(x, 2) + math.pow(y, 2)
            result += math.sqrt(z) * math.exp(-z / 1000)
        
        return result
    
    def matrix_operations(self, size: int = 2000, iterations: int = 100):
        """Heavy matrix operations"""
        matrices = [np.random.rand(size, size) for _ in range(10)]
        
        for _ in range(iterations):
            # Matrix multiplication chain
            result = matrices[0]
            for m in matrices[1:]:
                result = np.dot(result, m)
            
            # Heavy operations
            result = np.sin(result) + np.cos(result)
            result = np.sqrt(np.abs(result))
            result = np.linalg.inv(result + np.eye(size) * 0.1)
            
            # Update matrices
            matrices = [m + result * 0.01 for m in matrices]
        
        return result
    
    def continuous_cpu_load(self, target_load: float = 1.0, duration: float = 60.0):
        """Generate continuous CPU load"""
        self.running = True
        num_threads = int(self.max_workers * target_load)
        
        def cpu_worker():
            while self.running:
                # Heavy computation
                self.heavy_mathematical_computation(iterations=100000)
                time.sleep(0.001)  # Small sleep to prevent complete lockup
        
        self.workers = []
        for _ in range(num_threads):
            thread = threading.Thread(target=cpu_worker, daemon=True)
            thread.start()
            self.workers.append(thread)
        
        # Run for duration
        time.sleep(duration)
        self.stop()
    
    def stop(self):
        """Stop CPU-intensive work"""
        self.running = False
        for worker in self.workers:
            worker.join(timeout=1.0)
        self.workers = []

