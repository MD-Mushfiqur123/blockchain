"""
Simple Blockchain GUI without matplotlib dependency
Uses only tkinter (built-in)
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
import queue
from collections import deque

# Import blockchain components
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from blockchain.core.blockchain import Blockchain
    from blockchain.wallet.wallet import Wallet
    from blockchain.utils.miner import Miner
    from blockchain.utils.config import Config
    from blockchain.utils.logger import setup_logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)


class SimpleBlockchainGUI:
    """Simple GUI for blockchain visualization (no matplotlib)"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Blockchain - Real-time Monitor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize blockchain
        self.config = Config()
        self.blockchain = Blockchain(
            difficulty=self.config.get('blockchain.difficulty', 4),
            block_time_target=1.0
        )
        self.wallet = Wallet()
        self.miner = Miner(self.blockchain, self.wallet, threads=4)
        
        # Heavy compute components
        self.heavy_mode = False
        self.gpu_accelerator = None
        self.cpu_intensive = None
        self.power_consumer = None
        
        self.running = False
        self.update_queue = queue.Queue()
        
        # Statistics
        self.block_count = 0
        self.last_block_time = time.time()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg='#1e1e1e')
        title_frame.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🔗 Advanced Blockchain Monitor",
            font=("Arial", 24, "bold"),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        title_label.pack()
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg='#1e1e1e')
        control_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start Blockchain",
            command=self.start_blockchain,
            bg='#00aa00',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.heavy_btn = tk.Button(
            control_frame,
            text="🔥 Heavy Mode",
            command=self.start_heavy_mode,
            bg='#ff6600',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            bd=3
        )
        self.heavy_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop Blockchain",
            command=self.stop_blockchain,
            bg='#aa0000',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=30,
            pady=10,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg='#1e1e1e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Statistics
        left_panel = tk.Frame(content_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        stats_label = tk.Label(
            left_panel,
            text="📊 Statistics",
            font=("Arial", 16, "bold"),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        stats_label.pack(pady=10)
        
        self.stats_text = tk.Text(
            left_panel,
            height=20,
            bg='#1e1e1e',
            fg='#00ff00',
            font=("Courier", 11),
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right panel - Logs
        right_panel = tk.Frame(content_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        log_label = tk.Label(
            right_panel,
            text="📝 Blockchain Log",
            font=("Arial", 16, "bold"),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        log_label.pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            right_panel,
            height=20,
            bg='#1e1e1e',
            fg='#00ff00',
            font=("Courier", 10),
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Wallet info at bottom
        wallet_frame = tk.Frame(self.root, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        wallet_frame.pack(fill=tk.X, padx=10, pady=5)
        
        wallet_label = tk.Label(
            wallet_frame,
            text="💼 Wallet Information",
            font=("Arial", 12, "bold"),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        wallet_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.wallet_text = tk.Label(
            wallet_frame,
            text=f"Address: {self.wallet.get_address()[:50]}... | Balance: 0.00000000",
            font=("Courier", 10),
            bg='#2d2d2d',
            fg='#00ff00',
            anchor=tk.W
        )
        self.wallet_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
    def start_blockchain(self):
        """Start blockchain generation"""
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start blockchain thread
        self.blockchain_thread = threading.Thread(target=self.blockchain_worker, daemon=True)
        self.blockchain_thread.start()
        
        # Start UI update thread
        self.update_thread = threading.Thread(target=self.update_ui_worker, daemon=True)
        self.update_thread.start()
        
        self.log("🚀 Blockchain started!")
        self.log(f"💰 Wallet: {self.wallet.get_address()}")
    
    def start_heavy_mode(self):
        """Start heavy mode with maximum GPU/CPU usage"""
        import tkinter.messagebox as messagebox
        response = messagebox.askyesno(
            "Heavy Mode Warning",
            "⚠️ WARNING: Heavy mode will consume maximum CPU/GPU power!\n\n"
            "This will:\n"
            "- Use 100%+ of all CPU cores\n"
            "- Generate significant heat\n"
            "- Consume maximum power\n\n"
            "Ensure adequate cooling!\n\n"
            "Continue?"
        )
        
        if response:
            self.heavy_mode = True
            try:
                from blockchain.compute.gpu_accelerator import GPUAccelerator
                from blockchain.compute.cpu_intensive import CPUIntensive
                from blockchain.compute.power_consumer import PowerConsumer
                
                self.gpu_accelerator = GPUAccelerator()
                self.cpu_intensive = CPUIntensive()
                self.power_consumer = PowerConsumer()
                
                # Start heavy operations
                self.gpu_accelerator.continuous_gpu_work(duration=3600)
                
                heavy_thread = threading.Thread(
                    target=self.cpu_intensive.continuous_cpu_load,
                    args=(1.0, 3600),
                    daemon=True
                )
                heavy_thread.start()
                
                power_thread = threading.Thread(
                    target=self.power_consumer.maximum_power_mode,
                    args=(3600,),
                    daemon=True
                )
                power_thread.start()
                
                self.log("🔥 HEAVY MODE ENABLED - Maximum power consumption!")
                self.heavy_btn.config(state=tk.DISABLED, text="🔥 HEAVY MODE ACTIVE")
            except Exception as e:
                self.log(f"❌ Failed to start heavy mode: {e}")
                self.heavy_mode = False
    
    def stop_blockchain(self):
        """Stop blockchain generation"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        # Stop heavy mode if active
        if self.heavy_mode:
            if self.gpu_accelerator:
                self.gpu_accelerator.stop()
            if self.cpu_intensive:
                self.cpu_intensive.stop()
            if self.power_consumer:
                self.power_consumer.stop()
            self.heavy_mode = False
            self.heavy_btn.config(state=tk.NORMAL, text="🔥 Heavy Mode")
        
        self.log("⏹ Blockchain stopped!")
    
    def blockchain_worker(self):
        """Worker thread for blockchain operations"""
        last_block_time = time.time()
        target_interval = 1.0
        
        while self.running:
            try:
                current_time = time.time()
                elapsed = current_time - last_block_time
                
                if elapsed >= target_interval:
                    # Create and mine block
                    block = self.blockchain.create_block(self.wallet.get_address())
                    
                    if block:
                        start_mine = time.time()
                        if block.mine(max_iterations=1000000):
                            mine_time = time.time() - start_mine
                            
                            if self.blockchain.add_block(block):
                                actual_interval = time.time() - last_block_time
                                self.block_count += 1
                                
                                # Queue update
                                self.update_queue.put({
                                    'type': 'block',
                                    'block': block,
                                    'mine_time': mine_time,
                                    'interval': actual_interval
                                })
                                
                                last_block_time = time.time()
                
                time.sleep(0.01)
            except Exception as e:
                self.log(f"❌ Error: {e}")
                time.sleep(0.1)
    
    def update_ui_worker(self):
        """Worker thread for UI updates"""
        while self.running:
            try:
                # Process queued updates
                while not self.update_queue.empty():
                    update = self.update_queue.get_nowait()
                    if update['type'] == 'block':
                        self.root.after(0, self.update_block_info, update)
                
                # Update statistics
                self.root.after(0, self.update_statistics)
                
                time.sleep(0.5)
            except Exception as e:
                print(f"UI update error: {e}")
                time.sleep(0.1)
    
    def update_block_info(self, update):
        """Update block information in UI"""
        block = update['block']
        mine_time = update['mine_time']
        interval = update['interval']
        
        self.log(
            f"✅ Block #{block.index} | "
            f"Hash: {block.hash[:16]}... | "
            f"⛏️ Mine: {mine_time:.3f}s | "
            f"⏱️ Interval: {interval:.3f}s | "
            f"📊 Difficulty: {block.difficulty} | "
            f"📝 TXs: {len(block.transactions)}"
        )
    
    def update_statistics(self):
        """Update statistics display"""
        info = self.blockchain.get_chain_info()
        miner_stats = self.miner.get_stats()
        balance = self.blockchain.get_balance(self.wallet.get_address())
        
        stats = f"""
╔══════════════════════════════════════════╗
║     BLOCKCHAIN STATISTICS                ║
╠══════════════════════════════════════════╣
║ Chain Height:     {info['chain_height']:>20} ║
║ Difficulty:       {info['difficulty']:>20} ║
║ Total Supply:     {info['total_supply']:>18.8f} ║
║ Pending TXs:      {info['pending_transactions']:>20} ║
║ Blocks Mined:    {miner_stats['blocks_mined']:>20} ║
║ Hash Rate:       {miner_stats.get('hashes_per_second', 0):>18.2f} ║
║ Your Balance:     {balance:>18.8f} ║
║ Last Block:       {info['last_block_hash'][:20] if info['last_block_hash'] else 'N/A':>20} ║
╚══════════════════════════════════════════╝
        """
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
        
        # Update wallet info
        self.wallet_text.config(
            text=f"Address: {self.wallet.get_address()[:50]}... | Balance: {balance:.8f} BTC"
        )
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 200:
            self.log_text.delete(1.0, f"{len(lines) - 200}.0")


def main():
    """Main entry point for simple GUI"""
    root = tk.Tk()
    app = SimpleBlockchainGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

