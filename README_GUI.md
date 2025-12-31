# Blockchain GUI - Visual Interface

## Features

- **Real-time Blockchain Visualization**: Watch blocks being created in real-time
- **Live Statistics**: Chain height, difficulty, supply, and more
- **Interactive Charts**: 4 real-time charts showing:
  - Block height over time
  - Mining difficulty
  - Block time intervals
  - Transactions per block
- **Wallet Information**: View your wallet address and balance
- **Live Logging**: See all blockchain events as they happen
- **Start/Stop Controls**: Control blockchain generation

## Running the GUI

### Option 1: Direct Run
```bash
python run_gui.py
```

### Option 2: Import and Run
```python
from gui.blockchain_gui import main
main()
```

## GUI Components

### Left Panel
- **Controls**: Start/Stop buttons
- **Statistics**: Real-time blockchain stats
- **Wallet**: Your wallet address and balance

### Right Panel
- **Logs**: Real-time blockchain event log
- **Charts**: 4 animated charts showing blockchain metrics

## Charts

1. **Block Height**: Shows the growth of the blockchain
2. **Mining Difficulty**: Tracks difficulty adjustments
3. **Block Time**: Shows time between blocks (target: 1 second)
4. **Transactions**: Number of transactions per block

## Requirements

The GUI requires:
- `tkinter` (usually included with Python)
- `matplotlib` (for charts)
- All blockchain dependencies

Install with:
```bash
pip install -r requirements.txt
```

## Usage Tips

1. Click "Start Blockchain" to begin block generation
2. Watch the charts update in real-time
3. Monitor statistics in the left panel
4. View detailed logs in the right panel
5. Click "Stop Blockchain" to pause generation

## Performance

The GUI runs blockchain operations in background threads to keep the interface responsive. Charts update every second with new data.

