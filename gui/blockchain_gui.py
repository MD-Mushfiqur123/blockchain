"""
Advanced Blockchain GUI with real-time visualization
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
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


class BlockchainGUI:
    """Advanced GUI for blockchain visualization"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Blockchain - Real-time Monitor")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize blockchain
        self.config = Config()
        self.blockchain = Blockchain(
            difficulty=self.config.get('blockchain.difficulty', 4),
            block_time_target=1.0
        )
        self.wallet = Wallet()
        self.miner = Miner(self.blockchain, self.wallet, threads=4)
        
        self.running = False
        self.update_queue = queue.Queue()
        
        # Data for plotting
        self.block_times = deque(maxlen=100)
        self.block_heights = deque(maxlen=100)
        self.difficulty_history = deque(maxlen=100)
        self.transaction_counts = deque(maxlen=100)
        
        self.setup_ui()
        self.setup_plots()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Controls and Info
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Title
        title_label = tk.Label(
            left_panel, 
            text="🔗 Advanced Blockchain Monitor", 
            font=("Arial", 20, "bold"),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Control buttons
        control_frame = ttk.LabelFrame(left_panel, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start Blockchain",
            command=self.start_blockchain,
            bg='#00aa00',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.start_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop Blockchain",
            command=self.stop_blockchain,
            bg='#aa0000',
            fg='white',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(left_panel, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.stats_text = tk.Text(
            stats_frame,
            height=15,
            width=40,
            bg='#2d2d2d',
            fg='#00ff00',
            font=("Courier", 10),
            wrap=tk.WORD
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # Wallet info
        wallet_frame = ttk.LabelFrame(left_panel, text="Wallet", padding="10")
        wallet_frame.pack(fill=tk.X, pady=5)
        
        self.wallet_text = tk.Text(
            wallet_frame,
            height=5,
            width=40,
            bg='#2d2d2d',
            fg='#00ff00',
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.wallet_text.pack(fill=tk.X)
        self.update_wallet_info()
        
        # Right panel - Visualizations
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Log output
        log_frame = ttk.LabelFrame(right_panel, text="Blockchain Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=20,
            bg='#1e1e1e',
            fg='#00ff00',
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
    def setup_plots(self):
        """Setup matplotlib plots"""
        # Create plot frame
        plot_frame = ttk.LabelFrame(self.root, text="Real-time Charts", padding="10")
        plot_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # Create figure with subplots
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(14, 8))
        self.fig.patch.set_facecolor('#1e1e1e')
        
        # Configure axes
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.set_facecolor('#2d2d2d')
            ax.tick_params(colors='#00ff00')
            ax.spines['bottom'].set_color('#00ff00')
            ax.spines['top'].set_color('#00ff00')
            ax.spines['right'].set_color('#00ff00')
            ax.spines['left'].set_color('#00ff00')
            ax.xaxis.label.set_color('#00ff00')
            ax.yaxis.label.set_color('#00ff00')
            ax.title.set_color('#00ff00')
        
        # Plot 1: Block Height over Time
        self.ax1.set_title('Block Height', color='#00ff00', fontsize=12, fontweight='bold')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Height')
        self.line1, = self.ax1.plot([], [], color='#00ff00', linewidth=2)
        
        # Plot 2: Difficulty
        self.ax2.set_title('Mining Difficulty', color='#00ff00', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Block')
        self.ax2.set_ylabel('Difficulty')
        self.line2, = self.ax2.plot([], [], color='#ff0000', linewidth=2)
        
        # Plot 3: Block Time
        self.ax3.set_title('Block Time (seconds)', color='#00ff00', fontsize=12, fontweight='bold')
        self.ax3.set_xlabel('Block')
        self.ax3.set_ylabel('Time (s)')
        self.line3, = self.ax3.plot([], [], color='#0000ff', linewidth=2)
        
        # Plot 4: Transactions per Block
        self.ax4.set_title('Transactions per Block', color='#00ff00', fontsize=12, fontweight='bold')
        self.ax4.set_xlabel('Block')
        self.ax4.set_ylabel('Count')
        self.line4, = self.ax4.plot([], [], color='#ffff00', linewidth=2)
        
        plt.tight_layout()
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update_plots, interval=1000, blit=False)
        
    def update_plots(self, frame):
        """Update plots with new data"""
        if len(self.block_heights) == 0:
            return
        
        # Update plot 1: Block Height
        x1 = list(range(len(self.block_heights)))
        y1 = list(self.block_heights)
        self.line1.set_data(x1, y1)
        self.ax1.relim()
        self.ax1.autoscale_view()
        
        # Update plot 2: Difficulty
        x2 = list(range(len(self.difficulty_history)))
        y2 = list(self.difficulty_history)
        self.line2.set_data(x2, y2)
        self.ax2.relim()
        self.ax2.autoscale_view()
        
        # Update plot 3: Block Time
        x3 = list(range(len(self.block_times)))
        y3 = list(self.block_times)
        self.line3.set_data(x3, y3)
        self.ax3.relim()
        self.ax3.autoscale_view()
        
        # Update plot 4: Transactions
        x4 = list(range(len(self.transaction_counts)))
        y4 = list(self.transaction_counts)
        self.line4.set_data(x4, y4)
        self.ax4.relim()
        self.ax4.autoscale_view()
        
        self.canvas.draw()
    
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
        
        self.log("Blockchain started!")
    
    def stop_blockchain(self):
        """Stop blockchain generation"""
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("Blockchain stopped!")
    
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
                                
                                # Update data for plots
                                self.block_heights.append(block.index)
                                self.difficulty_history.append(block.difficulty)
                                self.block_times.append(actual_interval)
                                self.transaction_counts.append(len(block.transactions))
                                
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
                self.log(f"Error: {e}")
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
            f"Block {block.index} | "
            f"Hash: {block.hash[:16]}... | "
            f"Mine: {mine_time:.3f}s | "
            f"Interval: {interval:.3f}s | "
            f"Difficulty: {block.difficulty} | "
            f"TXs: {len(block.transactions)}"
        )
    
    def update_statistics(self):
        """Update statistics display"""
        info = self.blockchain.get_chain_info()
        miner_stats = self.miner.get_stats()
        
        stats = f"""
╔══════════════════════════════════════╗
║     BLOCKCHAIN STATISTICS            ║
╠══════════════════════════════════════╣
║ Chain Height: {info['chain_height']:>20} ║
║ Difficulty:   {info['difficulty']:>20} ║
║ Total Supply: {info['total_supply']:>18.8f} ║
║ Pending TXs:  {info['pending_transactions']:>20} ║
║ Blocks Mined: {miner_stats['blocks_mined']:>20} ║
║ Hash Rate:    {miner_stats.get('hashes_per_second', 0):>18.2f} ║
║ Last Block:   {info['last_block_hash'][:16] if info['last_block_hash'] else 'N/A':>20} ║
╚══════════════════════════════════════╝
        """
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def update_wallet_info(self):
        """Update wallet information"""
        balance = self.blockchain.get_balance(self.wallet.get_address())
        wallet_info = f"""
Address: {self.wallet.get_address()[:40]}...
Balance: {balance:.8f} BTC
        """
        
        self.wallet_text.delete(1.0, tk.END)
        self.wallet_text.insert(1.0, wallet_info)
        
        # Update periodically
        if self.running:
            self.root.after(2000, self.update_wallet_info)
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.log_text.delete(1.0, f"{len(lines) - 100}.0")


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

