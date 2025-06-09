from alphavantage_mcp_server.api import fetch_quote, fetch_time_series_daily, fetch_time_series_weekly

class AlphavantageAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_quote(self, symbol):
        response = fetch_quote(symbol=symbol, api_key=self.api_key)
        return response

    def get_daily_time_series(self, symbol):
        response = fetch_time_series_daily(symbol=symbol, api_key=self.api_key)
        return response

    def get_weekly_time_series(self, symbol):
        response = fetch_time_series_weekly(symbol=symbol, api_key=self.api_key)
        return response

    def fetch_data(self, query):
        # Implement logic to parse the query and call the appropriate method
        pass