from web3 import Web3
from src.services.telegram_notification import send_telegram_message
from src.services.mongodb import add_deposit_info
from src.dto.deposit import Deposit
from src.logging_config import logger
from src.services.whatsapp_alerts import send_whatsapp_message


def save_deposit_info(tx, block):
    """
    Processes and saves deposit information, logs details, and sends notifications via Telegram and WhatsApp.

    Args:
    tx (dict): A dictionary containing transaction data. Expected to include 'gasPrice', 'gas', 'hash', and 'from'.
    block (dict): A dictionary containing block data. Expected to include 'number' and 'timestamp'.

    Returns:
    None

    Raises:
    Exception: Logs and re-raises any exceptions encountered during processing.

    This function performs the following actions:
    1. Calculates the transaction fee using 'gasPrice' and 'gas' from the transaction data.
    2. Creates a `Deposit` object with the calculated fee and other transaction and block details.
    3. Logs the deposit information.
    4. Saves the deposit information to MongoDB.
    5. Prepares a notification message with deposit details.
    6. Sends the notification message via Telegram and WhatsApp.
    """
    try:
        # Calculate the transaction fee
        fee = tx['gasPrice'] * tx['gas']

        deposit_data = {
            'blockNumber': block['number'],
            'blockTimestamp': block['timestamp'],
            'fee': Web3.from_wei(fee, 'ether'),
            'hash': tx['hash'].hex(),
            'pubkey': tx['from']
        }

        # Create a Deposit object from the raw data
        deposit = Deposit(
            block_number=deposit_data['blockNumber'],
            block_timestamp=deposit_data['blockTimestamp'],
            fee=deposit_data['fee'],
            transaction_hash=deposit_data['hash'],
            pubkey=deposit_data['pubkey']
        )

        # Log the deposit info and save it to MongoDB
        logger.info(f"Saving deposit info: {deposit_data}")
        add_deposit_info(deposit.to_dict())

        # Prepare and send the Telegram and WhatsApp message
        message = (f"New ETH Deposit Detected!\n"
                   f"Block Number: {deposit.block_number}\n"
                   f"Timestamp: {deposit.block_timestamp}\n"
                   f"Sender: {deposit.pubkey}\n"
                   f"Amount: {deposit.fee} ETH\n"
                   f"Transaction Hash: {deposit.transaction_hash}")

        send_telegram_message(message)
        send_whatsapp_message(message)
        logger.info(f"Telegram and WhatsApp messages sent: {message}")

    except Exception as e:
        logger.error(f"Error in saving deposit info: {e}")
        raise
