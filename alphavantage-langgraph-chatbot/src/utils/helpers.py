def fetch_api_key():
    import os
    return os.getenv("ALPHAVANTAGE_API_KEY")

def format_response(data):
    if isinstance(data, dict):
        return json.dumps(data, indent=4)
    return str(data)

def log_message(message):
    import logging
    logging.basicConfig(level=logging.INFO)
    logging.info(message)

def validate_symbol(symbol):
    if not isinstance(symbol, str) or len(symbol) == 0:
        raise ValueError("Invalid stock symbol provided.")
    return symbol.upper()