"""
Advanced features and optimizations
"""
from .merkle_proof import MerkleProof, verify_merkle_proof
from .script_engine import ScriptEngine
from .consensus import ConsensusEngine

__all__ = ['MerkleProof', 'verify_merkle_proof', 'ScriptEngine', 'ConsensusEngine']

