from datetime import datetime
from src.logging_config import logger  # Import the logger from root configuration

class Deposit:
    def __init__(self, block_number, block_timestamp, fee, transaction_hash, pubkey):
        """
        Initialize a Deposit instance with the provided details.

        Args:
        block_number (int): The block number in which the deposit was recorded.
        block_timestamp (datetime): The timestamp when the block was created.
        fee (int): The transaction fee associated with the deposit (in Wei).
        transaction_hash (str): The hash of the transaction that represents the deposit.
        pubkey (str): The public key of the sender.

        Logs an informational message about the creation of the Deposit instance.
        """
        self.block_number = block_number
        self.block_timestamp = block_timestamp
        self.fee = fee
        self.transaction_hash = transaction_hash
        self.pubkey = pubkey

        logger.info(f"Deposit created: Block {block_number}, Transaction {transaction_hash}")

    def to_dict(self):
        """
        Convert the Deposit object into a dictionary format.

        Returns:
        dict: A dictionary representation of the Deposit instance, suitable for MongoDB storage.

        Logs an informational message about the conversion of the Deposit to a dictionary.
        """
        deposit_dict = {
            'blockNumber': self.block_number,
            'blockTimestamp': self.block_timestamp,
            'fee': self.fee,
            'hash': self.transaction_hash,
            'pubkey': self.pubkey,
        }
        logger.info(f"Converted Deposit to dict: {deposit_dict}")
        return deposit_dict

    @classmethod
    def from_event(cls, event, block, transaction, transaction_receipt):
        """
        Create a Deposit instance from blockchain event data.

        Args:
        event (dict): The event data from the blockchain transaction.
        block (dict): The block data containing the transaction information.
        transaction (dict): The transaction data associated with the event.
        transaction_receipt (dict): The receipt of the transaction, including gas usage.

        Returns:
        Deposit: An instance of the Deposit class created from the provided event data.

        Raises:
        Exception: If an error occurs during the creation of the Deposit instance, it is logged and re-raised.

        Logs an informational message about the creation of the Deposit from the event.
        """
        try:
            gas_used = int(transaction_receipt['gasUsed'], 16)
            gas_price = int(transaction['gasPrice'], 16)
            fee = gas_used * gas_price
            block_timestamp = datetime.utcfromtimestamp(int(block['timestamp'], 16))

            deposit = cls(
                block_number=event['blockNumber'],
                block_timestamp=block_timestamp,
                fee=fee,
                transaction_hash=event['transactionHash'],
                pubkey=event['args']['pubkey'].hex()
            )

            logger.info(
                f"Created Deposit from event: Block {event['blockNumber']}, Transaction {event['transactionHash']}")
            return deposit

        except Exception as e:
            logger.error(f"Error creating Deposit from event: {e}")
            raise
