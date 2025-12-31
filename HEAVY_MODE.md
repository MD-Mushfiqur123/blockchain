# 🔥 Heavy Mode - Maximum GPU/CPU Usage

## ⚠️ WARNING

**This mode will consume maximum CPU and GPU power!**

- High power consumption
- Significant heat generation
- May slow down other applications
- Ensure adequate cooling
- Use with caution

## Features

### GPU-Accelerated Operations
- Large matrix computations (5000x5000+)
- Parallel hash operations
- GPU-like mining acceleration
- Continuous heavy matrix work

### CPU-Intensive Operations
- Multi-core parallel processing
- Heavy cryptographic work (millions of rounds)
- Complex mathematical computations
- Matrix operations using all CPU cores

### Power Consumption
- Maximum CPU load (100%+ on all cores)
- Continuous GPU-like operations
- Parallel mining across all cores
- Heavy post-block computations

## Usage

### Run Heavy Mode
```bash
python run_heavy.py
```

Or directly:
```bash
python main_heavy.py
```

## What It Does

1. **GPU Accelerator**: Continuous large matrix operations
2. **CPU Intensive**: Heavy computations on all CPU cores
3. **Parallel Miner**: Multi-process mining with maximum power
4. **Power Consumer**: Maximum power consumption mode

## Performance Impact

- **CPU Usage**: 100%+ on all cores
- **Memory**: High usage (several GB)
- **Power**: Maximum consumption
- **Heat**: Significant heat generation
- **Battery**: Drains quickly on laptops

## Recommendations

1. **Desktop Systems**: Ensure adequate cooling
2. **Laptops**: Use while plugged in
3. **Monitoring**: Watch temperatures
4. **Duration**: Limit runtime to prevent overheating
5. **Other Apps**: Close unnecessary applications

## Components

- `blockchain/compute/gpu_accelerator.py` - GPU-like operations
- `blockchain/compute/cpu_intensive.py` - CPU-intensive work
- `blockchain/compute/parallel_miner.py` - Heavy parallel mining
- `blockchain/compute/power_consumer.py` - Maximum power mode
- `main_heavy.py` - Heavy blockchain application

## Normal Mode

For normal usage without heavy computation:
```bash
python main.py          # Command line
python run_simple_gui.py  # Simple GUI
```

