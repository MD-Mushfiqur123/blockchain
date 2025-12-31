"""
Advanced mining system with multi-threading
"""
import threading
import time
from typing import Optional
from ..core.blockchain import Blockchain
from ..core.block import Block
from ..wallet.wallet import Wallet


class Miner:
    """Advanced miner with threading and optimization"""
    
    def __init__(self, blockchain: Blockchain, wallet: Wallet, threads: int = 4):
        self.blockchain = blockchain
        self.wallet = wallet
        self.threads = threads
        self.mining = False
        self.mining_threads: List[threading.Thread] = []
        self.stats = {
            'blocks_mined': 0,
            'total_time': 0.0,
            'hashes_per_second': 0.0
        }
    
    def start_mining(self):
        """Start mining with multiple threads"""
        if self.mining:
            return
        
        self.mining = True
        
        for i in range(self.threads):
            thread = threading.Thread(
                target=self._mining_worker,
                args=(i,),
                daemon=True
            )
            thread.start()
            self.mining_threads.append(thread)
    
    def stop_mining(self):
        """Stop mining"""
        self.mining = False
        for thread in self.mining_threads:
            thread.join(timeout=1.0)
        self.mining_threads = []
    
    def _mining_worker(self, thread_id: int):
        """Mining worker thread"""
        while self.mining:
            try:
                # Create block
                block = self.blockchain.create_block(self.wallet.get_address())
                
                if block:
                    # Mine block
                    start_time = time.time()
                    if block.mine():
                        end_time = time.time()
                        mining_time = end_time - start_time
                        
                        # Add to blockchain
                        if self.blockchain.add_block(block):
                            self.stats['blocks_mined'] += 1
                            self.stats['total_time'] += mining_time
                            
                            if mining_time > 0:
                                self.stats['hashes_per_second'] = (
                                    self.stats['blocks_mined'] / self.stats['total_time']
                                )
                            
                            print(f"Block {block.index} mined by thread {thread_id} in {mining_time:.2f}s")
                
                # Small delay to prevent CPU spinning
                time.sleep(0.01)
            except Exception as e:
                print(f"Mining error in thread {thread_id}: {e}")
                time.sleep(0.1)
    
    def get_stats(self) -> dict:
        """Get mining statistics"""
        return self.stats.copy()

