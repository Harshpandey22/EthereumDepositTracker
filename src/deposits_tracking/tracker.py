import asyncio
import json
import websockets
from src.deposits_tracking.blockchain_service import get_transaction, get_block
from src.deposits_tracking.deposit_saver import save_deposit_info
from src.logging_config import logger

async def track_deposits():
    """
    Monitors Ethereum blocks in real-time via WebSocket to track new deposits.

    This function establishes a WebSocket connection to the Ethereum mainnet, subscribes to mined transactions,
    and processes each transaction to identify deposits to a specific address. When a deposit is detected,
    the deposit information is saved, and a notification is sent.

    This process involves:
    1. Connecting to the WebSocket endpoint.
    2. Sending a subscription request to monitor transactions for a specific contract address.
    3. Listening for incoming transaction events.
    4. Fetching transaction and block details.
    5. Saving the deposit information and sending notifications.

    Returns:
    None

    Raises:
    Exception: Logs and re-raises any exceptions encountered during WebSocket communication or data processing.
    """
    websocket_url = "wss://eth-mainnet.g.alchemy.com/v2/6_VS6cbitVVEUR4QTc9102SrmRbJS0mb"

    try:
        # Establish WebSocket connection
        async with websockets.connect(websocket_url) as websocket:
            logger.info("Connected to WebSocket, subscribing to mined transactions...")

            # Send subscription request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_subscribe",
                "params": [
                    "alchemy_minedTransactions",
                    {
                        "addresses": [
                            {"to": "0x00000000219ab540356cBB839Cbe05303d7705Fa"},  # Deposit contract address
                        ],
                        "includeRemoved": False,
                        "hashesOnly": True,
                    },
                ],
            }

            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            logger.info(f"Subscribed successfully: {response}")

            # Listen for new transaction events
            while True:
                try:
                    message = await websocket.recv()
                    logger.info(f"Received event: {message}")
                    event_data = json.loads(message)

                    # Ensure event contains valid transaction data
                    if "params" in event_data and "result" in event_data["params"]:
                        tx_hash_info = event_data["params"]["result"]

                        # Extract the transaction hash
                        if isinstance(tx_hash_info, dict) and "transaction" in tx_hash_info:
                            tx_hash = tx_hash_info["transaction"]["hash"]
                        elif isinstance(tx_hash_info, str):  # Direct hash string
                            tx_hash = tx_hash_info
                        else:
                            logger.error("Invalid transaction format received")
                            continue

                        logger.info(f"Deposit detected in transaction {tx_hash}")

                        # Fetch transaction details using the transaction hash
                        transaction = get_transaction(tx_hash)

                        # Fetch the block using the block number from the transaction data
                        block_number = transaction["blockNumber"]
                        block = get_block(block_number)

                        # Call the method to save deposit info
                        save_deposit_info(transaction, block)

                except websockets.exceptions.ConnectionClosed as e:
                    logger.error(f"Connection closed: {e}")
                    break

    except Exception as e:
        logger.error(f"Error in WebSocket subscription: {e}")
        raise


# Start the tracking loop
asyncio.get_event_loop().run_until_complete(track_deposits())
