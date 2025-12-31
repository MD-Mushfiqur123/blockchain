"""
Heavy blockchain application with maximum GPU/CPU usage
WARNING: This will consume significant power and generate heat
"""
import time
import threading
from blockchain.core.blockchain import Blockchain
from blockchain.wallet.wallet import Wallet
from blockchain.utils.config import Config
from blockchain.utils.logger import setup_logger
from blockchain.compute.gpu_accelerator import GPUAccelerator
from blockchain.compute.cpu_intensive import CPUIntensive
from blockchain.compute.parallel_miner import ParallelMiner
from blockchain.compute.power_consumer import PowerConsumer

logger = setup_logger()


class HeavyBlockchainApplication:
    """Heavy blockchain with maximum computational power"""
    
    def __init__(self):
        self.config = Config()
        self.blockchain = Blockchain(
            difficulty=self.config.get('blockchain.difficulty', 4),
            block_time_target=1.0
        )
        self.wallet = Wallet()
        
        # Heavy compute components
        self.gpu_accelerator = GPUAccelerator()
        self.cpu_intensive = CPUIntensive()
        self.parallel_miner = ParallelMiner()
        self.power_consumer = PowerConsumer()
        
        self.running = False
        logger.warning("⚠️  HEAVY MODE: This will consume significant CPU/GPU power!")
    
    def start_heavy_blockchain(self):
        """Start heavy blockchain with maximum power consumption"""
        self.running = True
        
        logger.info("🔥 Starting HEAVY blockchain mode...")
        logger.info("⚡ Maximum CPU/GPU usage enabled")
        logger.info("🌡️  System may heat up - ensure adequate cooling!")
        
        # Start GPU work
        logger.info("🚀 Starting GPU-accelerated operations...")
        gpu_thread = self.gpu_accelerator.continuous_gpu_work(duration=3600)  # 1 hour
        
        # Start CPU-intensive work
        logger.info("💻 Starting CPU-intensive operations...")
        cpu_thread = threading.Thread(
            target=self.cpu_intensive.continuous_cpu_load,
            args=(1.0, 3600),
            daemon=True
        )
        cpu_thread.start()
        
        # Start power consumer
        logger.info("⚡ Starting maximum power consumption mode...")
        power_thread = threading.Thread(
            target=self.power_consumer.maximum_power_mode,
            args=(3600,),
            daemon=True
        )
        power_thread.start()
        
        # Heavy block generation
        logger.info("⛏️  Starting heavy block generation...")
        self.start_heavy_block_generation()
    
    def start_heavy_block_generation(self):
        """Generate blocks with heavy computation"""
        last_block_time = time.time()
        target_interval = 1.0
        
        while self.running:
            try:
                current_time = time.time()
                elapsed = current_time - last_block_time
                
                if elapsed >= target_interval:
                    # Create block
                    block = self.blockchain.create_block(self.wallet.get_address())
                    
                    if block:
                        # Heavy mining with GPU acceleration
                        logger.info(f"⛏️  Mining block {block.index} with HEAVY computation...")
                        start_mine = time.time()
                        
                        # Use parallel miner for heavy work
                        if self.parallel_miner.mine_block_heavy(block, max_iterations=5000000):
                            mine_time = time.time() - start_mine
                            
                            if self.blockchain.add_block(block):
                                actual_interval = time.time() - last_block_time
                                
                                logger.info(
                                    f"✅ Block {block.index} mined | "
                                    f"Hash: {block.hash[:16]}... | "
                                    f"⛏️  Mine: {mine_time:.3f}s | "
                                    f"⚡ Heavy computation complete"
                                )
                                
                                # Additional heavy computation after block
                                self.heavy_post_block_work(block)
                                
                                last_block_time = time.time()
                
                time.sleep(0.01)
            except Exception as e:
                logger.error(f"Error: {e}")
                time.sleep(0.1)
    
    def heavy_post_block_work(self, block):
        """Heavy computation after each block"""
        # Heavy matrix computation
        self.gpu_accelerator.heavy_matrix_computation(size=3000, iterations=10)
        
        # CPU-intensive work
        self.cpu_intensive.heavy_mathematical_computation(iterations=100000)
        
        # Parallel matrix chain
        self.power_consumer.parallel_matrix_chain(num_matrices=50, size=1500)
    
    def start_statistics(self):
        """Display statistics"""
        def stats_worker():
            while self.running:
                try:
                    time.sleep(10)
                    info = self.blockchain.get_chain_info()
                    
                    logger.info(
                        f"📊 Stats | "
                        f"Height: {info['chain_height']} | "
                        f"Difficulty: {info['difficulty']} | "
                        f"Supply: {info['total_supply']:.8f} | "
                        f"⚡ HEAVY MODE ACTIVE"
                    )
                except Exception as e:
                    logger.error(f"Stats error: {e}")
        
        thread = threading.Thread(target=stats_worker, daemon=True)
        thread.start()
    
    def run(self):
        """Run heavy blockchain"""
        logger.info("=" * 60)
        logger.info("🔥 HEAVY BLOCKCHAIN MODE")
        logger.info("=" * 60)
        logger.info("⚠️  WARNING: Maximum power consumption!")
        logger.info("🌡️  Ensure adequate cooling!")
        logger.info("=" * 60)
        
        # Start statistics
        self.start_statistics()
        
        # Start heavy blockchain
        self.start_heavy_blockchain()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down heavy mode...")
            self.stop()
    
    def stop(self):
        """Stop heavy operations"""
        self.running = False
        self.gpu_accelerator.stop()
        self.cpu_intensive.stop()
        self.parallel_miner.stop()
        self.power_consumer.stop()
        logger.info("Heavy mode stopped")


def main():
    """Main entry point"""
    app = HeavyBlockchainApplication()
    app.run()


if __name__ == '__main__':
    main()

