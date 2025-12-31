"""
Native/low-level implementations for performance
Simulates Rust, Go, and Assembly-like operations
"""
from .rust_simulator import RustSimulator
from .go_simulator import GoSimulator
from .assembly_simulator import AssemblySimulator

__all__ = ['RustSimulator', 'GoSimulator', 'AssemblySimulator']

