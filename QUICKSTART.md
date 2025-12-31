# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Blockchain

### Basic Usage

Run the main application:
```bash
python main.py
```

This will:
- Start generating blocks approximately every second
- Mine blocks with proof of work
- Create sample transactions automatically
- Display statistics every 10 seconds
- Run a P2P network node (optional)

### Example Usage

Run the example script:
```bash
python examples/basic_usage.py
```

## Configuration

Create a `config.json` file to customize:

```json
{
  "blockchain": {
    "difficulty": 4,
    "block_time_target": 1.0,
    "max_block_size": 1000000
  },
  "mining": {
    "threads": 4,
    "enabled": true
  },
  "network": {
    "host": "localhost",
    "port": 8333
  }
}
```

## Creating Wallets

```python
from blockchain.wallet.wallet import Wallet

# Create new wallet
wallet = Wallet()
print(f"Address: {wallet.get_address()}")

# Save wallet
wallet.save_to_file("my_wallet.json", password="mypassword")

# Load wallet
wallet = Wallet.load_from_file("my_wallet.json", password="mypassword")
```

## Creating Transactions

```python
from blockchain.core.blockchain import Blockchain
from blockchain.wallet.wallet import Wallet

blockchain = Blockchain()
wallet1 = Wallet()
wallet2 = Wallet()

# Mine some blocks to get coins
for i in range(5):
    blockchain.mine_block(wallet1.get_address())

# Get UTXOs
utxos = blockchain.utxo_set.get_utxos_for_address(wallet1.get_address())

# Create transaction
tx = wallet1.create_transaction(
    recipient_address=wallet2.get_address(),
    amount=1.0,
    utxos=utxos[:1],
    fee=0.001
)

# Add to blockchain
blockchain.add_transaction(tx)

# Mine block with transaction
blockchain.mine_block(wallet1.get_address())
```

## Checking Balance

```python
balance = blockchain.get_balance(wallet1.get_address())
print(f"Balance: {balance}")
```

## Network Usage

```python
from blockchain.network.node import Node
from blockchain.core.blockchain import Blockchain
import asyncio

blockchain = Blockchain()
node = Node(blockchain, host='localhost', port=8333)

# Start node
asyncio.run(node.start_server())

# Connect to peer
asyncio.run(node.connect_to_peer('localhost', 8334))
```

## Performance Monitoring

```python
from blockchain.performance.profiler import PerformanceProfiler

profiler = PerformanceProfiler()

with profiler.time_operation('mining'):
    block = blockchain.mine_block(wallet.get_address())

stats = profiler.get_stats()
print(stats)
```

## Security Auditing

```python
from blockchain.security.auditor import BlockchainAuditor

auditor = BlockchainAuditor(blockchain)
results = auditor.audit_chain()
print(results)

# Check for double spends
double_spends = auditor.check_double_spend()
print(f"Double spends found: {len(double_spends)}")
```

## Storage

```python
from blockchain.storage.database import BlockchainDatabase

# Create database
db = BlockchainDatabase('blockchain.db')

# Save block
db.save_block(block)

# Load block
block = db.load_block(0)

# Load entire chain
blocks = db.load_blockchain()
```

