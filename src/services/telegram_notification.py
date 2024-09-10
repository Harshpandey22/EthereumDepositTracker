import requests
import os
from dotenv import load_dotenv
from src.logging_config import logger

# Load environment variables from .env file
load_dotenv()

# Retrieve Telegram bot token and chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    """
    Sends a message to a specified Telegram chat using a bot.

    Parameters:
    message (str): The message content to be sent to the Telegram chat.

    Returns:
    None
    """
    try:
        # Define the URL for the Telegram API sendMessage endpoint
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        # Send the POST request to the Telegram API
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response indicates a successful message send
        if response.json().get("ok"):
            logger.info("Message sent successfully")
        else:
            logger.warning(f"Failed to send message: {response.json()}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error while sending message: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while sending message: {e}")
