# 🚀 Run.py - Master Launcher

## Overview

`run.py` is the **master launcher** that activates **ALL blockchain functions** simultaneously.

## Features Activated

### Core Functions
- ✅ Blockchain with UTXO model
- ✅ Block generation (~1 per second)
- ✅ Proof of Work mining
- ✅ Wallet management
- ✅ Transaction creation

### Advanced Functions
- ✅ Network node (P2P)
- ✅ Database persistence (SQLite)
- ✅ Performance profiling
- ✅ Metrics collection
- ✅ Security auditing
- ✅ Background services
- ✅ Worker pools

### Heavy Functions (Optional)
- ✅ GPU acceleration
- ✅ CPU-intensive operations
- ✅ Parallel mining
- ✅ Maximum power consumption

### Native Functions
- ✅ Rust-like operations
- ✅ Go-like concurrency
- ✅ Assembly-like bit operations

## Usage

### Basic Mode (All Functions)
```bash
python run.py
```

### Heavy Mode (Maximum Power)
```bash
python run.py --heavy
```

### GUI Mode
```bash
python run.py --gui
```

### GUI + Heavy Mode
```bash
python run.py --gui --heavy
```

## What Gets Activated

1. **Blockchain Core**: Full blockchain with block generation
2. **Mining**: Multi-threaded mining (8 threads)
3. **Network**: P2P node for block/transaction propagation
4. **Database**: SQLite persistence for all blocks
5. **Performance**: Profiling and metrics collection
6. **Security**: Continuous auditing and validation
7. **Background Services**: Service manager with multiple services
8. **Worker Pool**: Parallel work processing (8 workers)
9. **Transactions**: Automatic transaction creation
10. **Statistics**: Real-time statistics display
11. **Heavy Mode** (optional): Maximum GPU/CPU usage
12. **Native Ops** (optional): Rust/Go/Assembly operations

## Statistics Display

Every 10 seconds, displays:
- Chain height
- Difficulty
- Total supply
- Pending transactions
- Blocks mined
- Wallet balance
- Average block time
- Transaction throughput
- Performance metrics

## Heavy Mode Warning

When using `--heavy`:
- ⚠️ Maximum CPU/GPU usage
- ⚠️ High power consumption
- ⚠️ Significant heat generation
- ⚠️ Ensure adequate cooling

## Example Output

```
🚀 MASTER BLOCKCHAIN APPLICATION - ACTIVATING ALL FUNCTIONS
======================================================================
✅ All components initialized
💰 Wallet: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
🔧 ACTIVATING ALL FUNCTIONS...
📊 Starting performance profiler...
📈 Starting metrics collector...
⚙️  Starting background services...
👷 Starting worker pool...
🌐 Starting network node...
⛏️  Starting block generation...
💸 Starting transaction creation...
💾 Starting database persistence...
🔒 Starting security auditing...
📊 Starting statistics display...
✅ ALL FUNCTIONS ACTIVATED!
```

## Stopping

Press `Ctrl+C` to stop all functions gracefully.

All components will shut down:
- Services stopped
- Database closed
- Network disconnected
- Heavy mode disabled
- All threads terminated

## Requirements

All packages from `requirements.txt`:
- cryptography
- pycryptodome
- ecdsa
- base58
- aiohttp
- numpy
- scipy

## Performance

With all functions active:
- **CPU Usage**: High (especially with --heavy)
- **Memory**: Several GB
- **Network**: Active P2P connections
- **Disk**: SQLite database writes
- **Power**: High consumption

## Recommended Usage

- **Development/Testing**: `python run.py` (normal mode)
- **Production**: `python run.py` (all features)
- **Stress Testing**: `python run.py --heavy` (maximum power)
- **Visual Monitoring**: `python run.py --gui` (with GUI)

