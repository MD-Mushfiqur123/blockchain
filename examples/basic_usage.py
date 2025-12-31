"""
Basic usage examples for the blockchain
"""
from blockchain.core.blockchain import Blockchain
from blockchain.wallet.wallet import Wallet
from blockchain.utils.logger import setup_logger

logger = setup_logger()


def example_create_wallet():
    """Example: Create a wallet"""
    wallet = Wallet()
    logger.info(f"Created wallet with address: {wallet.get_address()}")
    return wallet


def example_create_transaction():
    """Example: Create a transaction"""
    blockchain = Blockchain()
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    # Mine some blocks to get coins
    for i in range(5):
        block = blockchain.mine_block(wallet1.get_address())
        if block:
            logger.info(f"Mined block {block.index}")
    
    # Get UTXOs
    utxos = blockchain.utxo_set.get_utxos_for_address(wallet1.get_address())
    logger.info(f"Wallet1 has {len(utxos)} UTXOs")
    
    if utxos:
        # Create transaction
        tx = wallet1.create_transaction(
            recipient_address=wallet2.get_address(),
            amount=1.0,
            utxos=utxos[:1],
            fee=0.001
        )
        
        if tx:
            logger.info(f"Created transaction: {tx['tx_id'][:16]}...")
            blockchain.add_transaction(tx)
            
            # Mine block with transaction
            block = blockchain.mine_block(wallet1.get_address())
            if block:
                logger.info(f"Mined block {block.index} with transaction")
        
        logger.info(f"Wallet1 balance: {blockchain.get_balance(wallet1.get_address())}")
        logger.info(f"Wallet2 balance: {blockchain.get_balance(wallet2.get_address())}")


def example_blockchain_info():
    """Example: Get blockchain information"""
    blockchain = Blockchain()
    
    # Mine some blocks
    wallet = Wallet()
    for i in range(10):
        blockchain.mine_block(wallet.get_address())
    
    info = blockchain.get_chain_info()
    logger.info(f"Blockchain info: {info}")


if __name__ == '__main__':
    logger.info("Running basic examples...")
    example_create_wallet()
    example_create_transaction()
    example_blockchain_info()

