"""
Maximum power consumption operations
Heavy GPU and CPU usage
"""
import threading
import time
import multiprocessing
import numpy as np
import hashlib
import math
from typing import List


class PowerConsumer:
    """Consume maximum CPU and GPU power"""
    
    def __init__(self):
        self.running = False
        self.threads = []
        self.processes = []
    
    def maximum_power_mode(self, duration: float = 300.0):
        """Enable maximum power consumption mode"""
        self.running = True
        
        num_cores = multiprocessing.cpu_count()
        
        # CPU-intensive threads
        def cpu_intensive_worker():
            while self.running:
                # Heavy mathematical computation
                result = 0.0
                for i in range(100000):
                    x = math.sin(i) * math.cos(i * 2)
                    y = math.sqrt(abs(x))
                    result += math.exp(-y)
                
                # Heavy hashing
                data = str(result).encode()
                for _ in range(1000):
                    data = hashlib.sha256(data).digest()
                    data = hashlib.sha3_256(data).digest()
        
        # GPU-like matrix operations
        def gpu_like_worker():
            while self.running:
                # Large matrix operations
                size = 3000
                a = np.random.rand(size, size)
                b = np.random.rand(size, size)
                
                # Heavy matrix chain
                for _ in range(10):
                    c = np.dot(a, b)
                    c = np.sin(c) + np.cos(c)
                    c = np.sqrt(np.abs(c))
                    a = c
                    b = np.dot(c, c.T)
        
        # Cryptographic work
        def crypto_worker():
            while self.running:
                data = np.random.bytes(1024)
                for _ in range(10000):
                    data = hashlib.sha256(data).digest()
                    data = hashlib.sha3_256(data).digest()
                    data = hashlib.blake2b(data, digest_size=32).digest()
        
        # Start threads (2x CPU cores for hyperthreading)
        for _ in range(num_cores * 2):
            t1 = threading.Thread(target=cpu_intensive_worker, daemon=True)
            t2 = threading.Thread(target=gpu_like_worker, daemon=True)
            t3 = threading.Thread(target=crypto_worker, daemon=True)
            
            t1.start()
            t2.start()
            t3.start()
            
            self.threads.extend([t1, t2, t3])
        
        # Run for duration
        time.sleep(duration)
        self.stop()
    
    def heavy_blockchain_computation(self, block_data: dict, iterations: int = 1000):
        """Heavy blockchain-specific computations"""
        results = []
        
        for i in range(iterations):
            # Heavy matrix computation
            matrix = np.random.rand(2000, 2000)
            matrix = np.dot(matrix, matrix.T)
            matrix = np.sin(matrix) + np.cos(matrix)
            matrix = np.linalg.inv(matrix + np.eye(2000) * 0.1)
            
            # Heavy hashing
            data = matrix.tobytes()
            for _ in range(100):
                data = hashlib.sha256(data).digest()
                data = hashlib.sha3_256(data).digest()
            
            # Cryptographic operations
            result = hashlib.sha256(data).hexdigest()
            results.append(result)
        
        return results
    
    def parallel_matrix_chain(self, num_matrices: int = 100, size: int = 1000):
        """Heavy parallel matrix chain computation"""
        matrices = [np.random.rand(size, size) for _ in range(num_matrices)]
        
        def compute_chain(start_idx, end_idx):
            result = matrices[start_idx]
            for i in range(start_idx + 1, end_idx):
                result = np.dot(result, matrices[i])
                result = np.sin(result) + np.cos(result)
            return result
        
        # Parallel computation
        num_workers = multiprocessing.cpu_count()
        chunk_size = num_matrices // num_workers
        
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.starmap(
                compute_chain,
                [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_workers)]
            )
        
        # Combine results
        final_result = results[0]
        for r in results[1:]:
            final_result = np.dot(final_result, r)
        
        return final_result
    
    def stop(self):
        """Stop all power-consuming operations"""
        self.running = False
        for thread in self.threads:
            thread.join(timeout=0.1)
        self.threads = []

