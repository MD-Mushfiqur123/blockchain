"""
Master launcher - Activates ALL blockchain functions
Comprehensive startup with all features enabled
"""
import sys
import os
import threading
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imsport all blockchain components
from blockchain.core.blockchain import Blockchain
from blockchain.wallet.wallet import Wallet
from blockchain.utils.miner import Miner
from blockchain.utils.config import Config
from blockchain.utils.logger import setup_logger
from blockchain.network.node import Node
from blockchain.storage.database import BlockchainDatabase
from blockchain.performance.profiler import PerformanceProfiler
from blockchain.performance.metrics import MetricsCollector
from blockchain.security.auditor import BlockchainAuditor
from blockchain.background.service_manager import ServiceManager
from blockchain.background.worker_pool import WorkerPool

# Import hedavy compute components
try:
    from blockchain.compute.gpu_accelerator import GPUAccelerator
    from blockchain.compute.cpu_intensive import CPUIntensive
    from blockchain.compute.parallel_miner import ParallelMiner
    from blockchain.compute.power_consumer import PowerConsumer
    HEAVY_AVAILABLE = True
except ImportError:
    HEAVY_AVAILABLE = False
    print("⚠️  Heavy compute modules not available")

# Import nadtive components
try:
    from blockchain.native.rust_simulator import RustSimulator
    from blockchain.native.go_simulator import GoSimulator
    from blockchain.native.assembly_simulator import AssemblySimulator
    NATIVE_AVAILABLE = True
except ImportError:
    NATIVE_AVAILABLE = False

logger = setup_logger()


class MasterBlockchainApplication:
    """Master application activating ALL functions"""
    
    def __init__(self):
        logger.info("=" * 70)
        logger.info("MASTER BLOCKCHAIN APPLICATION - ACTIVATING ALL FUNCTIONS")
        logger.info("=" * 70)
        
        # Core components
        self.config = Config()
        self.blockchain = Blockchain(
            difficulty=self.config.get('blockchain.difficulty', 4),
            block_time_target=1.0
        )
        self.wallet = Wallet()
        self.miner = Miner(self.blockchain, self.wallet, threads=8)
        
        # Storage
        self.database = BlockchainDatabase('blockchain.db')
        
        # Performance monitoring
        self.profiler = PerformanceProfiler()
        self.metrics = MetricsCollector()
        
        # Security
        self.auditor = BlockchainAuditor(self.blockchain)
        
        # Background services
        self.service_manager = ServiceManager()
        self.worker_pool = WorkerPool(num_workers=8)
        
        # Network
        self.node = None
        
        # Heavy compute (optional)
        if HEAVY_AVAILABLE:
            self.gpu_accelerator = GPUAccelerator()
            self.cpu_intensive = CPUIntensive()
            self.parallel_miner = ParallelMiner()
            self.power_consumer = PowerConsumer()
            self.heavy_mode = False
        else:
            self.heavy_mode = False
        
        # Native components
        if NATIVE_AVAILABLE:
            self.rust_sim = RustSimulator()
            self.go_sim = GoSimulator()
            self.assembly_sim = AssemblySimulator()
        
        # State
        self.running = False
        self.threads = []
        
        logger.info("[OK] All components initialized")
        logger.info(f"Wallet: {self.wallet.get_address()}")
    
    def activate_all_functions(self, heavy_mode: bool = False):
        """Activate ALL blockchain functions"""
        logger.info("=" * 70)
        logger.info("ACTIVATING ALL FUNCTIONS...")
        logger.info("=" * 70)
        
        self.running = True
        
        # 1. Start performance profiling
        logger.info("[1/12] Starting performance profiler...")
        self.profiler.enabled = True
        
        # 2. Start metrics collection
        logger.info("[2/12] Starting metrics collector...")
        metrics_thread = threading.Thread(target=self.metrics_worker, daemon=True)
        metrics_thread.start()
        self.threads.append(metrics_thread)
        
        # 3. Start background services
        logger.info("[3/12] Starting background services...")
        self.start_background_services()
        
        # 4. Start worker pool
        logger.info("[4/12] Starting worker pool...")
        self.worker_pool.start(self.worker_function)
        
        # 5. Start network node
        logger.info("[5/12] Starting network node...")
        self.start_network_node()
        
        # 6. Start block generation
        logger.info("[6/12] Starting block generation...")
        block_thread = threading.Thread(target=self.block_generation_worker, daemon=True)
        block_thread.start()
        self.threads.append(block_thread)
        
        # 7. Start transaction creation
        logger.info("[7/12] Starting transaction creation...")
        tx_thread = threading.Thread(target=self.transaction_worker, daemon=True)
        tx_thread.start()
        self.threads.append(tx_thread)
        
        # 8. Start database persistence
        logger.info("[8/12] Starting database persistence...")
        db_thread = threading.Thread(target=self.database_worker, daemon=True)
        db_thread.start()
        self.threads.append(db_thread)
        
        # 9. Start security auditing
        logger.info("[9/12] Starting security auditing...")
        audit_thread = threading.Thread(target=self.audit_worker, daemon=True)
        audit_thread.start()
        self.threads.append(audit_thread)
        
        # 10. Start statistics display
        logger.info("[10/12] Starting statistics display...")
        stats_thread = threading.Thread(target=self.statistics_worker, daemon=True)
        stats_thread.start()
        self.threads.append(stats_thread)
        
        # 11. Heavy mode (optional)
        if heavy_mode and HEAVY_AVAILABLE:
            logger.info("[11/12] ACTIVATING HEAVY MODE - Maximum GPU/CPU usage!")
            self.activate_heavy_mode()
        
        # 12. Native operations
        if NATIVE_AVAILABLE:
            logger.info("[12/12] Starting native operations (Rust/Go/Assembly)...")
            native_thread = threading.Thread(target=self.native_operations_worker, daemon=True)
            native_thread.start()
            self.threads.append(native_thread)
        
        logger.info("=" * 70)
        logger.info("[OK] ALL FUNCTIONS ACTIVATED!")
        logger.info("=" * 70)
    
    def start_background_services(self):
        """Start all background services"""
        # Register services
        self.service_manager.register_service('mining', self.mining_service)
        self.service_manager.register_service('validation', self.validation_service)
        self.service_manager.register_service('sync', self.sync_service)
        
        # Start all services
        self.service_manager.start_all()
    
    def mining_service(self):
        """Background mining service"""
        while self.running:
            try:
                time.sleep(0.1)
                # Service work
            except:
                break
    
    def validation_service(self):
        """Background validation service"""
        while self.running:
            try:
                time.sleep(0.1)
                # Validation work
            except:
                break
    
    def sync_service(self):
        """Background sync service"""
        while self.running:
            try:
                time.sleep(1.0)
                # Sync work
            except:
                break
    
    def start_network_node(self):
        """Start network node"""
        try:
            import asyncio
            self.node = Node(
                self.blockchain,
                host=self.config.get('network.host', 'localhost'),
                port=self.config.get('network.port', 8333)
            )
            
            def network_worker():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.node.start_server())
                loop.run_forever()
            
            network_thread = threading.Thread(target=network_worker, daemon=True)
            network_thread.start()
            self.threads.append(network_thread)
        except Exception as e:
            logger.warning(f"Network node not started: {e}")
    
    def block_generation_worker(self):
        """Generate blocks continuously"""
        last_block_time = time.time()
        target_interval = 1.0
        
        while self.running:
            try:
                with self.profiler.time_operation('block_creation'):
                    current_time = time.time()
                    elapsed = current_time - last_block_time
                    
                    if elapsed >= target_interval:
                        # Create block
                        block = self.blockchain.create_block(self.wallet.get_address())
                        
                        if block:
                            # Mine block
                            start_mine = time.time()
                            if block.mine(max_iterations=2000000):
                                mine_time = time.time() - start_mine
                                
                                if self.blockchain.add_block(block):
                                    actual_interval = time.time() - last_block_time
                                    
                                    # Update metrics
                                    self.metrics.record_block(block.size, len(block.transactions))
                                    
                                    # Save to database
                                    self.database.save_block(block)
                                    
                                    # Log
                                    logger.info(
                                        f"[OK] Block {block.index} | "
                                        f"Hash: {block.hash[:16]}... | "
                                        f"Mine: {mine_time:.3f}s | "
                                        f"TXs: {len(block.transactions)} | "
                                        f"Difficulty: {block.difficulty}"
                                    )
                                    
                                    last_block_time = time.time()
                
                time.sleep(0.01)
            except Exception as e:
                logger.error(f"Block generation error: {e}")
                time.sleep(0.1)
    
    def transaction_worker(self):
        """Create transactions periodically"""
        # Create additional wallets for testing
        wallet2 = Wallet()
        wallet3 = Wallet()
        
        while self.running:
            try:
                time.sleep(30)  # Create transaction every 30 seconds
                
                # Get UTXOs
                utxos = self.blockchain.utxo_set.get_utxos_for_address(self.wallet.get_address())
                
                if len(utxos) > 0 and utxos[0][2].get('amount', 0) > 1.0:
                    # Create transaction
                    tx = self.wallet.create_transaction(
                        recipient_address=wallet2.get_address(),
                        amount=0.5,
                        utxos=utxos[:1],
                        fee=0.001
                    )
                    
                    if tx:
                        if self.blockchain.add_transaction(tx):
                            logger.info(f"[TX] Transaction created: {tx['tx_id'][:16]}...")
                            
                            # Broadcast if node available
                            if self.node:
                                try:
                                    import asyncio
                                    loop = asyncio.get_event_loop()
                                    if loop.is_running():
                                        asyncio.create_task(self.node.broadcast_transaction(tx))
                                except:
                                    pass
            except Exception as e:
                logger.error(f"Transaction error: {e}")
                time.sleep(1.0)
    
    def database_worker(self):
        """Persist blocks to database (thread-safe)"""
        last_saved = 0
        
        while self.running:
            try:
                time.sleep(5)  # Save every 5 seconds
                
                # Save new blocks (thread-safe)
                with self.blockchain.lock:  # Use blockchain lock for thread safety
                    current_length = len(self.blockchain.chain)
                    for i in range(last_saved, current_length):
                        block = self.blockchain.chain[i]
                        try:
                            self.database.save_block(block)
                        except Exception as e:
                            logger.error(f"Database save error for block {i}: {e}")
                    
                    last_saved = current_length
            except Exception as e:
                logger.error(f"Database error: {e}")
                time.sleep(1.0)
    
    def audit_worker(self):
        """Run security audits periodically"""
        while self.running:
            try:
                time.sleep(60)  # Audit every minute
                
                # Run audit
                audit_results = self.auditor.audit_chain()
                
                if not audit_results['valid']:
                    logger.warning(f"[WARN] Audit found issues: {audit_results['errors']}")
                
                # Check for double spends
                double_spends = self.auditor.check_double_spend()
                if double_spends:
                    logger.warning(f"[WARN] Found {len(double_spends)} double spend attempts")
            except Exception as e:
                logger.error(f"Audit error: {e}")
                time.sleep(10.0)
    
    def statistics_worker(self):
        """Display statistics"""
        while self.running:
            try:
                time.sleep(10)  # Update every 10 seconds
                
                info = self.blockchain.get_chain_info()
                miner_stats = self.miner.get_stats()
                perf_stats = self.profiler.get_stats()
                metrics = self.metrics.get_metrics()
                balance = self.blockchain.get_balance(self.wallet.get_address())
                
                logger.info("=" * 70)
                logger.info("BLOCKCHAIN STATISTICS")
                logger.info("=" * 70)
                logger.info(f"Chain Height:     {info['chain_height']}")
                logger.info(f"Difficulty:       {info['difficulty']}")
                logger.info(f"Total Supply:     {info['total_supply']:.8f}")
                logger.info(f"Pending TXs:      {info['pending_transactions']}")
                logger.info(f"Blocks Mined:     {miner_stats['blocks_mined']}")
                logger.info(f"Your Balance:     {balance:.8f}")
                logger.info(f"Avg Block Time:   {metrics.get('average_block_time', 0):.3f}s")
                logger.info(f"Throughput:       {metrics.get('throughput_tps', 0):.2f} TX/s")
                if perf_stats:
                    logger.info(f"Performance:      {len(perf_stats)} operations profiled")
                logger.info("=" * 70)
            except Exception as e:
                logger.error(f"Statistics error: {e}")
                time.sleep(10.0)
    
    def metrics_worker(self):
        """Collect metrics continuously"""
        while self.running:
            try:
                time.sleep(1.0)
                # Metrics are updated when blocks are created
            except:
                break
    
    def worker_function(self, work_item):
        """Worker pool function"""
        # Process work items
        return f"Processed: {work_item}"
    
    def activate_heavy_mode(self):
        """Activate heavy GPU/CPU mode"""
        if not HEAVY_AVAILABLE:
            logger.warning("Heavy mode not available")
            return
        
        self.heavy_mode = True
        logger.warning("[HEAVY] HEAVY MODE: Maximum power consumption!")
        
        # Start GPU work
        self.gpu_accelerator.continuous_gpu_work(duration=3600)
        
        # Start CPU-intensive work
        cpu_thread = threading.Thread(
            target=self.cpu_intensive.continuous_cpu_load,
            args=(1.0, 3600),
            daemon=True
        )
        cpu_thread.start()
        self.threads.append(cpu_thread)
        
        # Start power consumer
        power_thread = threading.Thread(
            target=self.power_consumer.maximum_power_mode,
            args=(3600,),
            daemon=True
        )
        power_thread.start()
        self.threads.append(power_thread)
    
    def native_operations_worker(self):
        """Run native operations (Rust/Go/Assembly)"""
        if not NATIVE_AVAILABLE:
            return
        
        while self.running:
            try:
                time.sleep(5)
                
                # Rust-like operations
                test_data = b"test_data_for_native_ops"
                rust_hash = self.rust_sim.fast_hash(test_data)
                
                # Go-like operations
                ch = self.go_sim.Channel()
                self.go_sim.goroutine(lambda: ch.send("test"))
                
                # Assembly-like operations
                value = 12345
                rotated = self.assembly_sim.bit_rotate_left(value, 7, 32)
                
            except Exception as e:
                logger.debug(f"Native operations: {e}")
                time.sleep(1.0)
    
    def run(self, heavy_mode: bool = False):
        """Run master application"""
        try:
            # Activate all functions
            self.activate_all_functions(heavy_mode=heavy_mode)
            
            # Keep running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n" + "=" * 70)
            logger.info("SHUTTING DOWN...")
            logger.info("=" * 70)
            self.stop()
    
    def stop(self):
        """Stop all functions"""
        self.running = False
        
        # Stop services
        self.service_manager.stop_all()
        self.worker_pool.stop()
        
        # Stop heavy mode
        if self.heavy_mode and HEAVY_AVAILABLE:
            self.gpu_accelerator.stop()
            self.cpu_intensive.stop()
            self.power_consumer.stop()
        
        # Close database
        self.database.close()
        
        # Stop network
        if self.node:
            self.node.stop()
        
        logger.info("[OK] All functions stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Master Blockchain Application')
    parser.add_argument(
        '--heavy',
        action='store_true',
        help='Enable heavy mode (maximum GPU/CPU usage)'
    )
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch GUI instead of command line'
    )
    
    args = parser.parse_args()
    
    if args.gui:
        # Launch GUI
        try:
            from gui.simple_gui import main as gui_main
            gui_main()
        except ImportError:
            print("GUI not available, using command line mode")
            app = MasterBlockchainApplication()
            app.run(heavy_mode=args.heavy)
    else:
        # Command line mode
        app = MasterBlockchainApplication()
        
        if args.heavy:
            print("=" * 70)
            print("WARNING: Heavy mode will consume maximum CPU/GPU power!")
            print("Ensure adequate cooling!")
            print("=" * 70)
            response = input("Continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Cancelled.")
                return
        
        app.run(heavy_mode=args.heavy)


if __name__ == '__main__':
    main()

