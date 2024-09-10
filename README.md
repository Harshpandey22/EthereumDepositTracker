
# Ethereum Deposit Tracker

## Project Overview
The Ethereum Deposit Tracker is a real-time Ethereum blockchain monitoring tool that tracks deposit transactions, logs them, and sends notifications. This project leverages WebSocket for live transaction data, MongoDB for persistent storage, and integrates with Telegram and WhatsApp for real-time alerts.



## Features

 - Real-time Monitoring: Tracks Ethereum deposit transactions as they occur.
 - Data Storage: Saves transaction data in MongoDB for historical analysis.
 - Notifications: Sends real-time notifications via Telegram and WhatsApp.
 - WebSocket Subscription: Uses WebSocket to subscribe to new transactions on the Ethereum network.
 - Logging: Comprehensive logging of events and errors.

## Prerequisites
Before you begin, ensure you have the following:

 - Python 3.8 or higher
 - MongoDB instance (local or cloud-based like MongoDB Atlas)
 - Twilio account for WhatsApp messaging  (additionall)
 - Telegram bot for sending messages

## Use Cases
### Monitoring Deposits
Scenario: Track deposits on the Beacon Deposit Contract
 - (0x00000000219ab540356cBB839Cbe05303d7705Fa).

Solution: Establish an RPC connection and monitor deposit events. Record details in MongoDB.

### Tracking Specific Transactions
Scenario: Track specific deposits like:

- 0x1391be19259f10e01336a383217cf35344dd7aa157e95030f46235448ef5e5d6
 - 0x53c98c3371014fd54275ebc90a6e42dffa2eee427915cab5f80f1e3e9c64eba4
Solution: Fetch and store transaction details, including amount and sender address.

### Error Handling and Logging
Scenario: Ensure errors are managed and events are logged.

Solution: Implement robust error handling and logging for debugging and tracking.

### Real-time Alerts and Visualization
Scenario: Receive alerts and visualize deposit data.

Solution: Optionally integrate Telegram notifications and Grafana for real-time data visualization.


## Installation

### Clone the Repository

 ~~~ 
git clone https://github.com/yourusername/ethereum-deposit-tracker.git
cd ethereum-deposit-tracker 
~~~

### Set up a virtual environment:

~~~
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
~~~


### Install required dependencies:

~~~
pip install -r requirements.txt
~~~

### Set Up Environment Variables
Create a .env file in the root directory and add the following configuration:

~~~
ATLAS_URI=<your_mongodb_uri>
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
CHAT_ID=<your_telegram_chat_id>
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
~~~
Replace placeholders with your actual credentials.

### Configuration
 - MongoDB URI: Ensure your MongoDB instance is running and accessible from your environment.
 - Telegram Bot: Create a Telegram bot using BotFather and get the bot token. Add your bot to a chat and get the chat ID.
 - Twilio Account: Set up a Twilio account and obtain credentials for sending WhatsApp messages.

## Usage 

### Start the Deposit Tracking Service
~~~
python src/deposits_tracking/main.py
~~~

### Run the WebSocket Subscription
~~~
python src/deposits_tracking/track_deposits.py
~~~
## Logging
Logs are stored in the logs directory. The logging configuration is set to create a new log file every hour based on the timestamp. Both file and console logging are enabled.


