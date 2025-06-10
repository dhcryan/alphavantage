import os

class Config:
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "IZLU4YURP1R1YVYW")
    BASE_URL = "https://www.alphavantage.co/query"
    TIMEOUT = 10  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    @staticmethod
    def get_api_key():
        return Config.ALPHAVANTAGE_API_KEY

    @staticmethod
    def get_base_url():
        return Config.BASE_URL

    @staticmethod
    def get_timeout():
        return Config.TIMEOUT

    @staticmethod
    def get_max_retries():
        return Config.MAX_RETRIES

    @staticmethod
    def get_retry_delay():
        return Config.RETRY_DELAY