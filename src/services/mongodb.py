import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from src.logging_config import logger

# Load environment variables from a .env file
load_dotenv()

# MongoDB URI from environment variables
uri = os.getenv("MONGO_URI")

# Initialize MongoDB client with server API version
client = MongoClient(uri, server_api=ServerApi('1'))

# Reference to the database and collection
db = client['EthereumDepositTracker']
collection = db["Deposits"]

def health_check():
    """
    Performs a health check to verify the connection to MongoDB.

    Returns:
    str: A message indicating the connection status.
    """
    try:
        # Ping the MongoDB server to check connection
        client.admin.command('ping')
        logger.info("Pinged your deployment. Successfully connected to MongoDB!")
        return "Successfully connected to MongoDB!"
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return f"An error occurred: {e}"

def add_deposit_info(deposit):
    """
    Adds deposit information to the MongoDB collection.

    Parameters:
    deposit (dict): A dictionary containing deposit details.

    Returns:
    str: A message indicating the result of the insertion operation.
    """
    try:
        # Insert the deposit data into the MongoDB collection
        result = collection.insert_one(deposit)
        logger.info(f"Inserted document with _id: {result.inserted_id}")
        return f"Inserted document with _id: {result.inserted_id}"
    except Exception as e:
        logger.error(f"Error while inserting deposit: {e}")
        return f"An error occurred: {e}"

def get_all_deposits():
    """
    Retrieves all deposit documents from the MongoDB collection.

    Returns:
    list: A list of dictionaries, each representing a deposit document.
    """
    try:
        # Fetch all documents from the collection
        deposits = list(collection.find({}))
        logger.info(f"Retrieved {len(deposits)} deposits from the database.")

        # Convert MongoDB ObjectId to string for easier handling
        for deposit in deposits:
            deposit['_id'] = str(deposit['_id'])

        return deposits
    except Exception as e:
        logger.error(f"Error retrieving deposits: {e}")
        return f"An error occurred: {e}"
