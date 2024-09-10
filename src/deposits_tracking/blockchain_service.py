from web3 import Web3
from src.logging_config import logger

# Alchemy API URL for Ethereum mainnet
alchemy_url = "https://eth-mainnet.g.alchemy.com/v2/6_VS6cbitVVEUR4QTc9102SrmRbJS0mb"
web3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check Ethereum network connection
if web3.is_connected():
    logger.info("Successfully connected to Ethereum network.")
else:
    logger.error("Failed to connect to Ethereum network.")

def get_transaction(tx_hash):
    """
    Fetches the details of a specific transaction from the Ethereum blockchain using its hash.

    Args:
    tx_hash (str): The hash of the transaction to retrieve.

    Returns:
    dict: A dictionary containing the transaction details such as block number, from address, to address, value, etc.

    Raises:
    Exception: If an error occurs while fetching the transaction, it is logged and re-raised.
    """
    try:
        # Get transaction details using the Web3 client
        transaction = web3.eth.get_transaction(tx_hash)
        return transaction
    except Exception as e:
        logger.error(f"Error fetching transaction {tx_hash}: {e}")
        raise

def get_latest_block():
    """
    Retrieves the latest block number on the Ethereum blockchain.

    Returns:
    int: The number of the most recent block on the Ethereum blockchain.

    Logs the block number when successfully retrieved.
    """
    latest_block = web3.eth.block_number
    logger.info(f"Latest block number retrieved: {latest_block}")
    return latest_block

def get_block(block_number):
    """
    Fetches the details of a specific block from the Ethereum blockchain.

    Args:
    block_number (int): The number of the block to retrieve.

    Returns:
    dict: A dictionary containing details of the block, including transactions if `full_transactions=True` is set.

    Raises:
    Exception: If an error occurs while fetching the block, it is logged and re-raised.
    """
    try:
        block = web3.eth.get_block(block_number, full_transactions=True)
        logger.info(f"Block {block_number} retrieved successfully.")
        return block
    except Exception as e:
        logger.error(f"Error fetching block {block_number}: {e}")
        raise