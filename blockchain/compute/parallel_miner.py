"""
Heavy parallel mining using all CPU cores and GPU-like operations
Maximum power consumption
"""
import multiprocessing
import threading
import time
import hashlib
import numpy as np
from typing import Optional, Dict
from ..core.block import Block


class ParallelMiner:
    """Heavy parallel mining with maximum CPU/GPU usage"""
    
    def __init__(self, num_processes: int = None, num_threads_per_process: int = 4):
        self.num_processes = num_processes or multiprocessing.cpu_count()
        self.num_threads_per_process = num_threads_per_process
        self.running = False
        self.processes = []
    
    def mine_block_heavy(self, block: Block, max_iterations: int = 10000000) -> bool:
        """Heavy mining with maximum computational power"""
        target = '0' * block.difficulty
        
        def mining_process(process_id, start_nonce, end_nonce, result_queue):
            """Mining process with heavy computation"""
            best_nonce = None
            best_hash = None
            
            for nonce in range(start_nonce, end_nonce):
                if not self.running:
                    break
                
                # Heavy pre-computation
                # Create large computation matrix
                matrix_size = 500
                matrix = np.random.randint(0, 256, size=(matrix_size, matrix_size), dtype=np.uint8)
                
                # Heavy matrix operations (simulating GPU work)
                for _ in range(50):
                    matrix = np.dot(matrix, matrix.T) % 256
                    matrix = np.bitwise_xor(matrix, np.roll(matrix, 1))
                    matrix = (matrix * nonce) % 256
                
                # Update block
                block.nonce = nonce
                block.extra_nonce = (nonce // 1000) % 1000000
                block.header.nonce = nonce
                block.header.extra_nonce = block.extra_nonce
                block.header.timestamp = time.time()
                
                # Hash with matrix result
                matrix_hash = hashlib.sha256(matrix.tobytes()).digest()
                block_hash = block.header.hash()
                
                # Additional heavy hash rounds
                for _ in range(20):
                    block_hash_bytes = bytes.fromhex(block_hash)
                    block_hash = hashlib.sha256(block_hash_bytes).hexdigest()
                
                if block_hash[:block.difficulty] == target:
                    result_queue.put((nonce, block_hash))
                    return True
            
            return False
        
        # Split work across processes
        chunk_size = max_iterations // self.num_processes
        result_queue = multiprocessing.Queue()
        
        processes = []
        for i in range(self.num_processes):
            start = i * chunk_size
            end = start + chunk_size if i < self.num_processes - 1 else max_iterations
            process = multiprocessing.Process(
                target=mining_process,
                args=(i, start, end, result_queue)
            )
            process.start()
            processes.append(process)
        
        # Wait for result
        try:
            nonce, block_hash = result_queue.get(timeout=300)  # 5 minute timeout
            block.nonce = nonce
            block.hash = block_hash
            
            # Stop all processes
            for p in processes:
                p.terminate()
                p.join(timeout=1.0)
            
            return True
        except:
            # Timeout or no result
            for p in processes:
                p.terminate()
                p.join(timeout=1.0)
            return False
    
    def continuous_mining(self, blocks_queue, results_queue):
        """Continuous heavy mining process"""
        self.running = True
        
        while self.running:
            try:
                block = blocks_queue.get(timeout=1.0)
                if block is None:
                    break
                
                # Heavy mining
                success = self.mine_block_heavy(block, max_iterations=5000000)
                results_queue.put((block, success))
            except:
                continue
    
    def start_mining_pool(self, blocks_queue, results_queue):
        """Start mining pool with multiple processes"""
        processes = []
        for _ in range(self.num_processes):
            process = multiprocessing.Process(
                target=self.continuous_mining,
                args=(blocks_queue, results_queue)
            )
            process.start()
            processes.append(process)
        
        self.processes = processes
        return processes
    
    def stop(self):
        """Stop all mining processes"""
        self.running = False
        for process in self.processes:
            process.terminate()
            process.join(timeout=2.0)

