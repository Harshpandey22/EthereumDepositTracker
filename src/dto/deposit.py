from datetime import datetime

class Deposit:
    def __init__(self, block_number, block_timestamp, fee, transaction_hash, pubkey):
        """
        Initialize a Deposit instance.

        Parameters:
        block_number (int): The block number where the deposit was recorded.
        block_timestamp (datetime): The timestamp when the block was created.
        fee (float): The transaction fee in Ether.
        transaction_hash (str): The hash of the transaction.
        pubkey (str): The public key of the sender.
        """
        self.block_number = block_number
        self.block_timestamp = block_timestamp
        self.fee = float(fee)
        self.transaction_hash = transaction_hash
        self.pubkey = pubkey

    def to_dict(self):
        """
        Convert the Deposit instance to a dictionary for MongoDB storage.

        Returns:
        dict: A dictionary representation of the Deposit instance, with keys:
              'blockNumber', 'blockTimestamp', 'fee', 'hash', and 'pubkey'.
        """
        return {
            'blockNumber': self.block_number,
            'blockTimestamp': self.block_timestamp,
            'fee': self.fee,
            'hash': self.transaction_hash,
            'pubkey': self.pubkey,
        }

    @classmethod
    def from_event(cls, event, block, transaction, transaction_receipt):
        """
        Create a Deposit instance from blockchain event data.

        Parameters:
        event (dict): The event data containing deposit information.
        block (dict): The block data containing the block's timestamp.
        transaction (dict): The transaction data containing gas price.
        transaction_receipt (dict): The receipt data containing gas used.

        Returns:
        Deposit: An instance of the Deposit class populated with the extracted data.
        """
        # Calculate the gas fee (in Wei)
        gas_used = int(transaction_receipt['gasUsed'], 16)
        gas_price = int(transaction['gasPrice'], 16)
        fee = gas_used * gas_price

        # Convert the block timestamp from Unix time (seconds since epoch) to datetime
        block_timestamp = datetime.utcfromtimestamp(int(block['timestamp'], 16))

        return cls(
            block_number=event['blockNumber'],
            block_timestamp=block_timestamp,
            fee=fee,
            transaction_hash=event['transactionHash'],
            pubkey=event['args']['pubkey'].hex()  # Convert bytes to hex string
        )
