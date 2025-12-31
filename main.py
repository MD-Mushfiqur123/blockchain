"""
Main blockchain application - Generates blocks every second
Advanced Bitcoin-like blockchain implementation
"""
import asyncio
import time
import threading
from blockchain.core.blockchain import Blockchain
from blockchain.wallet.wallet import Wallet
from blockchain.utils.miner import Miner
from blockchain.utils.config import Config
from blockchain.utils.logger import setup_logger
from blockchain.network.node import Node

logger = setup_logger()


class BlockchainApplication:
    """Main blockchain application with automatic block generation"""
    
    def __init__(self):
        self.config = Config()
        self.blockchain = Blockchain(
            difficulty=self.config.get('blockchain.difficulty', 4),
            block_time_target=self.config.get('blockchain.block_time_target', 1.0)
        )
        self.wallet = Wallet()
        self.miner = Miner(
            self.blockchain,
            self.wallet,
            threads=self.config.get('mining.threads', 4)
        )
        self.node = None
        self.running = False
        self.block_generation_thread = None
        self.stats_thread = None
        
        logger.info(f"Blockchain initialized with difficulty {self.blockchain.difficulty}")
        logger.info(f"Wallet address: {self.wallet.get_address()}")
    
    def start_block_generation(self):
        """Start automatic block generation every second"""
        self.running = True
        
        def generate_blocks():
            """Block generation loop"""
            last_block_time = time.time()
            target_interval = self.config.get('blockchain.block_time_target', 1.0)
            
            while self.running:
                try:
                    current_time = time.time()
                    elapsed = current_time - last_block_time
                    
                    # Generate block if enough time has passed
                    if elapsed >= target_interval:
                        # Create and mine block
                        block = self.blockchain.create_block(self.wallet.get_address())
                        
                        if block:
                            start_mine = time.time()
                            if block.mine(max_iterations=5000000):  # Increased iterations
                                mine_time = time.time() - start_mine
                                
                                if self.blockchain.add_block(block):
                                    actual_interval = time.time() - last_block_time
                                    logger.info(
                                        f"Block {block.index} created | "
                                        f"Hash: {block.hash[:16]}... | "
                                        f"Mining time: {mine_time:.3f}s | "
                                        f"Interval: {actual_interval:.3f}s | "
                                        f"Difficulty: {self.blockchain.difficulty} | "
                                        f"Transactions: {len(block.transactions)}"
                                    )
                                    
                                    # Broadcast block if node is running (async handled in node)
                                    if self.node and hasattr(self.node, 'running') and self.node.running:
                                        try:
                                            loop = asyncio.get_event_loop()
                                            if loop.is_running():
                                                asyncio.create_task(self.node.broadcast_block(block))
                                        except:
                                            pass
                                    
                                    last_block_time = time.time()
                                else:
                                    logger.warning(f"Failed to add block {block.index}")
                            else:
                                logger.warning(f"Failed to mine block {block.index}")
                    
                    # Small sleep to prevent CPU spinning
                    time.sleep(0.01)
                except Exception as e:
                    logger.error(f"Error in block generation: {e}")
                    time.sleep(0.1)
        
        self.block_generation_thread = threading.Thread(target=generate_blocks, daemon=True)
        self.block_generation_thread.start()
        logger.info("Block generation started - creating blocks every ~1 second")
    
    def start_stats_monitoring(self):
        """Start statistics monitoring"""
        def monitor_stats():
            while self.running:
                try:
                    time.sleep(10)  # Print stats every 10 seconds
                    info = self.blockchain.get_chain_info()
                    miner_stats = self.miner.get_stats()
                    
                    logger.info(
                        f"=== Blockchain Stats ===\n"
                        f"Chain Height: {info['chain_height']}\n"
                        f"Difficulty: {info['difficulty']}\n"
                        f"Total Supply: {info['total_supply']:.8f}\n"
                        f"Pending Transactions: {info['pending_transactions']}\n"
                        f"Blocks Mined: {miner_stats['blocks_mined']}\n"
                        f"Wallet Balance: {self.wallet.get_balance():.8f}\n"
                        f"========================"
                    )
                except Exception as e:
                    logger.error(f"Error in stats monitoring: {e}")
        
        self.stats_thread = threading.Thread(target=monitor_stats, daemon=True)
        self.stats_thread.start()
    
    async def start_network(self):
        """Start P2P network node"""
        self.node = Node(
            self.blockchain,
            host=self.config.get('network.host', 'localhost'),
            port=self.config.get('network.port', 8333)
        )
        
        # Start server in background
        server_task = asyncio.create_task(self.node.start_server())
        logger.info("Network node started")
        return server_task
    
    def create_sample_transactions(self):
        """Create sample transactions for testing"""
        # Create additional wallets
        wallet2 = Wallet()
        wallet3 = Wallet()
        
        logger.info(f"Created test wallets:")
        logger.info(f"  Wallet 2: {wallet2.get_address()}")
        logger.info(f"  Wallet 3: {wallet3.get_address()}")
        
        # Wait for some blocks to be mined first
        time.sleep(5)
        
        # Create transactions periodically
        def create_transactions():
            while self.running:
                try:
                    time.sleep(30)  # Create transaction every 30 seconds
                    
                    # Get wallet UTXOs
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
                                logger.info(f"Transaction created: {tx['tx_id'][:16]}...")
                                if self.node and hasattr(self.node, 'running') and self.node.running:
                                    try:
                                        loop = asyncio.get_event_loop()
                                        if loop.is_running():
                                            asyncio.create_task(self.node.broadcast_transaction(tx))
                                    except:
                                        pass
                except Exception as e:
                    logger.error(f"Error creating transaction: {e}")
        
        tx_thread = threading.Thread(target=create_transactions, daemon=True)
        tx_thread.start()
    
    def run(self):
        """Run the blockchain application"""
        logger.info("=" * 60)
        logger.info("Starting Advanced Blockchain Application")
        logger.info("=" * 60)
        
        # Start block generation
        self.start_block_generation()
        
        # Start statistics monitoring
        self.start_stats_monitoring()
        
        # Start sample transaction creation
        self.create_sample_transactions()
        
        # Start network (async) - run in separate thread
        def start_network_async():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.start_network())
                loop.run_forever()
            except Exception as e:
                logger.warning(f"Network not started: {e}")
        
        network_thread = threading.Thread(target=start_network_async, daemon=True)
        network_thread.start()
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.stop()
    
    def stop(self):
        """Stop the application"""
        self.running = False
        self.miner.stop_mining()
        if self.node:
            self.node.stop()
        logger.info("Application stopped")


def main():
    """Main entry point"""
    app = BlockchainApplication()
    app.run()


if __name__ == '__main__':
    main()

