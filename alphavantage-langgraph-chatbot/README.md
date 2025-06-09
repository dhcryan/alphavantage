# alphavantage-langgraph-chatbot

## Overview
The Alphavantage LangGraph Chatbot is an interactive chatbot application that leverages the Alphavantage API to provide users with financial data and analysis. The chatbot is designed to facilitate easy access to various financial metrics, including stock quotes, time series data, and economic indicators.

## Project Structure
```
alphavantage-langgraph-chatbot
├── src
│   ├── main.py                # Entry point for the chatbot application
│   ├── graph                  # Module for managing the graph structure
│   │   ├── __init__.py
│   │   ├── nodes.py           # Defines the Node class for the graph
│   │   ├── edges.py           # Defines the Edge class for the graph
│   │   └── state.py           # Manages the state of the graph
│   ├── agents                 # Module for chatbot agents
│   │   ├── __init__.py
│   │   ├── alphavantage_agent.py  # Interacts with the Alphavantage API
│   │   └── analysis_agent.py      # Processes and analyzes data
│   ├── tools                  # Module for utility functions
│   │   ├── __init__.py
│   │   └── alphavantage_tools.py  # Functions for interacting with the API
│   ├── models                 # Module for data models
│   │   ├── __init__.py
│   │   └── schemas.py         # Defines data schemas and validation
│   └── utils                  # Module for utility helpers
│       ├── __init__.py
│       └── helpers.py         # Helper functions for various tasks
├── config
│   └── settings.py            # Configuration settings for the application
├── requirements.txt           # Project dependencies
├── .env.example               # Example environment variables
└── README.md                  # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/alphavantage-langgraph-chatbot.git
   cd alphavantage-langgraph-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to `.env` and update the `ALPHAVANTAGE_API_KEY` with your own API key.

4. Run the application:
   ```
   python src/main.py
   ```

## Usage
Once the application is running, you can interact with the chatbot through the command line. You can ask for various financial data, and the chatbot will respond with the relevant information fetched from the Alphavantage API.

## Examples
- "What is the current stock price of AAPL?"
- "Show me the historical data for TSLA."
- "What are the latest economic indicators?"

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.