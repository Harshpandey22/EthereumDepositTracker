from src.deposits_tracking.tracker import track_deposits
from src.logging_config import logger

def main():
    """
    Main entry point for the deposit tracking script.

    Initializes the logger and starts the deposit tracking process.
    """
    try:
        logger.info("Started Tracking")
        track_deposits()
    except Exception as e:
        logger.error(f"Error in deposit tracking: {e}")
        raise

if __name__ == "__main__":
    main()