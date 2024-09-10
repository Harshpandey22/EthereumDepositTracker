import os
import logging
import datetime

# Define the logs directory relative to the project root (one level up from the current script's directory)
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

# Create the logs folder if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create log file name based on the current date and time
log_file_name = datetime.datetime.now().strftime(f"{log_dir}/%Y-%m-%d_%H-%M-%S.log")

# Configure logging to write to the log file and the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_name),  # Log to file
        logging.StreamHandler()              # Log to console
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)