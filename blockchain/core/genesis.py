"""
Genesis block creation with complex initialization
"""
from .block import Block
import time


def create_genesis_block() -> Block:
    """Create genesis block with initial coin distribution"""
    genesis_transaction = {
        'tx_id': '0' * 64,  # Special genesis transaction ID
        'inputs': [],
        'outputs': [{
            'address': 'genesis_address_00000000000000000000000000000000',
            'amount': 0.0,  # No initial coins in genesis
            'script_pubkey': 'OP_GENESIS'
        }],
        'is_coinbase': True,
        'is_genesis': True
    }
    
    genesis_block = Block(
        index=0,
        transactions=[genesis_transaction],
        previous_hash='0' * 64,  # No previous block
        difficulty=4,
        nonce=0
    )
    
    # Set specific timestamp for genesis
    genesis_block.timestamp = time.time()
    genesis_block.hash = genesis_block.header.hash()
    
    return genesis_block

