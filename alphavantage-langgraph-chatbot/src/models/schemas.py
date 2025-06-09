from pydantic import BaseModel
from typing import List, Optional

class StockQuote(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    price: float
    volume: int
    latest_trading_day: str
    previous_close: float
    change: float
    change_percent: float

class TimeSeriesData(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class TimeSeriesDaily(BaseModel):
    symbol: str
    data: List[TimeSeriesData]

class CompanyOverview(BaseModel):
    symbol: str
    name: str
    sector: str
    industry: str
    description: str
    website: str
    market_cap: float
    dividend_yield: Optional[float] = None

class EarningsCalendar(BaseModel):
    symbol: str
    earnings_date: str
    estimated_eps: float
    reported_eps: float
    surprise: float

class EconomicIndicator(BaseModel):
    indicator_name: str
    value: float
    date: str
    frequency: str
    unit: str