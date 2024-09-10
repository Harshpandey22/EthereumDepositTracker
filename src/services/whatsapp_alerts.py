import os
from twilio.rest import Client
from src.logging_config import logger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials and configuration
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_number = 'whatsapp:+14155238886'  # Your Twilio sandbox number
recipient_number = 'whatsapp:+918874328862'  # Recipient's WhatsApp number

# Initialize Twilio client
client = Client(account_sid, auth_token)

def send_whatsapp_message(message):
    """
    Sends a WhatsApp message using Twilio.

    Parameters:
    message (str): The content of the message to send.

    Returns:
    None
    """
    try:
        # Create and send the message
        client.messages.create(
            body=message,
            from_=whatsapp_number,
            to=recipient_number
        )
        logger.info(f"WhatsApp message sent successfully: {message}")
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        raise
