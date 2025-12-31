"""
Heavy computational operations requiring GPU and CPU power
"""
from .gpu_accelerator import GPUAccelerator
from .cpu_intensive import CPUIntensive
from .parallel_miner import ParallelMiner
from .power_consumer import PowerConsumer

__all__ = ['GPUAccelerator', 'CPUIntensive', 'ParallelMiner', 'PowerConsumer']

