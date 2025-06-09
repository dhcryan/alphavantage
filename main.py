from mcp.server import FastMCP
from alpha_vantage.alphaintelligence import AlphaIntelligence
from alpha_vantage.commodities import Commodities
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.econindicators import EconIndicators
from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.options import Options
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries

mcp = FastMCP("alphavantage-mcp")


@mcp.tool()
def get_intraday(symbol: str, interval: str = '15min', outputsize: str = 'compact',
                 month: str = None, extended_hours: str = 'true', adjusted: str = 'true', entitlement=None):
    """ Return intraday time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min'
            (default '15min')
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length intraday times
            series, commonly above 1MB (default 'compact')
        month: If not None, specify a year and month to get data, supported
            format is YYYY-MM. For example "2009-01" (default None)
        extended_hours: By default, extended_hours=true and the output time series
            will include both the regular trading hours and the extended trading hours
            (4:00am to 8:00pm Eastern Time for the US market). Set extended_hours=false
            to query regular trading hours (9:30am to 4:00pm US Eastern Time) only.
            (default 'true')
        adjusted: By default, adjusted=true and the output time series is adjusted by
            historical split and dividend events. Set adjusted=false to
            query raw (as-traded) intraday values.
            (default 'true')
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ts = TimeSeries(output_format='json')
    return ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize, month=month,
                           extended_hours=extended_hours, adjusted=adjusted, entitlement=entitlement)


@mcp.tool()
def get_daily(symbol, outputsize='compact'):
    """ Return daily time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length daily times
            series, commonly above 1MB (default 'compact')
    """
    ts = TimeSeries(output_format='json')
    return ts.get_daily(symbol=symbol, outputsize=outputsize)


@mcp.tool()
def get_daily_adjusted(symbol, outputsize='compact', entitlement=None):
    """ Return daily adjusted (date, daily open, daily high, daily low,
    daily close, daily split/dividend-adjusted close, daily volume)
    time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length daily times
            series, commonly above 1MB (default 'compact')
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ts = TimeSeries(output_format='json')
    return ts.get_daily_adjusted(symbol=symbol, outputsize=outputsize, entitlement=entitlement)


@mcp.tool()
def get_weekly(symbol):
    """ Return weekly time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data

    """
    ts = TimeSeries(output_format='json')
    return ts.get_weekly(symbol=symbol)


@mcp.tool()
def get_weekly_adjusted(symbol):
    """  weekly adjusted time series (last trading day of each week,
    weekly open, weekly high, weekly low, weekly close, weekly adjusted
    close, weekly volume, weekly dividend) of the equity specified,
    covering up to 20 years of historical data.
    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data

    """
    ts = TimeSeries(output_format='json')
    return ts.get_weekly_adjusted(symbol=symbol)


@mcp.tool()
def get_monthly(symbol):
    """ Return monthly time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data

    """
    ts = TimeSeries(output_format='json')
    return ts.get_monthly(symbol=symbol)


@mcp.tool()
def get_monthly_adjusted(symbol):
    """ Return monthly time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data

    """
    ts = TimeSeries(output_format='json')
    return ts.get_monthly_adjusted(symbol=symbol)


@mcp.tool()
def get_quote_endpoint(symbol, entitlement=None):
    """ Return the latest price and volume information for a
     security of your choice

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ts = TimeSeries(output_format='json')
    return ts.get_quote_endpoint(symbol=symbol, entitlement=entitlement)


@mcp.tool()
def get_symbol_search(keywords):
    """ Return best matching symbols and market information
    based on keywords. It raises ValueError when problems arise

    Keyword Arguments:
        keywords: the keywords to query on

    """
    ts = TimeSeries(output_format='json')
    return ts.get_symbol_search(keywords=keywords)


@mcp.tool()
def get_market_status():
    """ Return current market status (open vs. closed) of major trading venues.
    It raises ValueError when problems arise
    """
    ts = TimeSeries(output_format='json')
    return ts.get_market_status()


@mcp.tool()
def get_company_overview(symbol):
    """
    Returns the company information, financial ratios,
    and other key metrics for the equity specified.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_company_overview(symbol=symbol)


@mcp.tool()
def get_dividends(symbol):
    """
    Returns historical and future (declared) dividend distributions.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_dividends(symbol=symbol)


@mcp.tool()
def get_splits(symbol):
    """
    Returns historical split events.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_splits(symbol=symbol)


@mcp.tool()
def get_income_statement_annual(symbol):
    """
    Returns the annual and quarterly income statements for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_income_statement_annual(symbol=symbol)


@mcp.tool()
def get_income_statement_quarterly(symbol):
    """
    Returns the annual and quarterly income statements for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_income_statement_quarterly(symbol=symbol)


@mcp.tool()
def get_balance_sheet_annual(symbol):
    """
    Returns the annual and quarterly balance sheets for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_balance_sheet_annual(symbol=symbol)


@mcp.tool()
def get_balance_sheet_quarterly(symbol):
    """
    Returns the annual and quarterly balance sheets for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_balance_sheet_quarterly(symbol=symbol)


@mcp.tool()
def get_cash_flow_annual(symbol):
    """
    Returns the annual and quarterly cash flows for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_cash_flow_annual(symbol=symbol)


@mcp.tool()
def get_cash_flow_quarterly(symbol):
    """
    Returns the annual and quarterly cash flows for the company of interest.
    Data is generally refreshed on the same day a company reports its latest
    earnings and financials.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_cash_flow_quarterly(symbol=symbol)


@mcp.tool()
def get_earnings_annual(symbol):
    """
    Returns the annual and quarterly earnings (EPS) for the company of interest.
    Quarterly data also includes analyst estimates and surprise metrics.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_earnings_annual(symbol=symbol)


@mcp.tool()
def get_earnings_quarterly(symbol):
    """
    Returns the annual and quarterly earnings (EPS) for the company of interest.
    Quarterly data also includes analyst estimates and surprise metrics.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
    """
    fd = FundamentalData(output_format='json')
    return fd.get_earnings_quarterly(symbol=symbol)


@mcp.tool()
def get_sma(self, symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return simple moving average time series in two json objects as data and
    meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_sma(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_ema(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return exponential moving average time series in two json objects
    as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ema(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_wma(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return weighted moving average time series in two json objects
    as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_wma(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_dema(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return double exponential moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_dema(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                       entitlement=entitlement)


@mcp.tool()
def get_tema(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return triple exponential moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_tema(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                       entitlement=entitlement)


@mcp.tool()
def get_trima(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return triangular moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_trima(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                        entitlement=entitlement)


@mcp.tool()
def get_kama(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return Kaufman adaptative moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_kama(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                       entitlement=entitlement)


@mcp.tool()
def get_mama(symbol, interval='daily', series_type='close',
             fastlimit=None, slowlimit=None, month=None, entitlement=None):
    """ Return MESA adaptative moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastlimit:  Positive floats for the fast limit are accepted
            (default=None)
        slowlimit:  Positive floats for the slow limit are accepted
            (default=None)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_mama(symbol=symbol, interval=interval, series_type=series_type, fastlimit=fastlimit,
                       slowlimit=slowlimit, month=month, entitlement=entitlement)


@mcp.tool()
def get_vwap(symbol, interval='5min', month=None, entitlement=None):
    """ Returns the volume weighted average price (VWAP) for intraday time series.

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min'
            (default 5min)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_vwap(symbol=symbol, interval=interval, month=month, entitlement=entitlement)


@mcp.tool()
def get_t3(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return triple exponential moving average time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_t3(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                     entitlement=entitlement)


@mcp.tool()
def get_macd(symbol, interval='daily', series_type='close',
             fastperiod=None, slowperiod=None, signalperiod=None, month=None, entitlement=None):
    """ Return the moving average convergence/divergence time series in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily'
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod:  Positive integers are accepted (default=None)
        slowperiod:  Positive integers are accepted (default=None)
        signalperiod:  Positive integers are accepted (default=None)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_macd(symbol=symbol, interval=interval, series_type=series_type, fastperiod=fastperiod,
                       slowperiod=slowperiod, signalperiod=signalperiod, month=month, entitlement=entitlement)


@mcp.tool()
def get_macdext(symbol, interval='daily', series_type='close',
                fastperiod=None, slowperiod=None, signalperiod=None, fastmatype=None,
                slowmatype=None, signalmatype=None, month=None, entitlement=None):
    """ Return the moving average convergence/divergence time series in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod:  Positive integers are accepted (default=None)
        slowperiod:  Positive integers are accepted (default=None)
        signalperiod:  Positive integers are accepted (default=None)
        fastmatype:  Moving average type for the faster moving average.
            By default, fastmatype=0. Integers 0 - 8 are accepted
            (check  down the mappings) or the string containing the math type can
            also be used.
        slowmatype:  Moving average type for the slower moving average.
            By default, slowmatype=0. Integers 0 - 8 are accepted
            (check down the mappings) or the string containing the math type can
            also be used.
        signalmatype:  Moving average type for the signal moving average.
            By default, signalmatype=0. Integers 0 - 8 are accepted
            (check down the mappings) or the string containing the math type can
            also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_macdext(symbol=symbol, interval=interval, series_type=series_type, fastperiod=fastperiod,
                          slowperiod=slowperiod, signalperiod=signalperiod, fastmatype=fastmatype,
                          slowmatype=slowmatype, signalmatype=signalmatype, month=month, entitlement=entitlement)


@mcp.tool()
def get_stoch(symbol, interval='daily', fastkperiod=None,
              slowkperiod=None, slowdperiod=None, slowkmatype=None, slowdmatype=None, month=None, entitlement=None):
    """ Return the stochatic oscillator values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        fastkperiod:  The time period of the fastk moving average. Positive
            integers are accepted (default=None)
        slowkperiod:  The time period of the slowk moving average. Positive
            integers are accepted (default=None)
        slowdperiod: The time period of the slowd moving average. Positive
            integers are accepted (default=None)
        slowkmatype:  Moving average type for the slowk moving average.
            By default, fastmatype=0. Integers 0 - 8 are accepted
            (check  down the mappings) or the string containing the math type can
            also be used.
        slowdmatype:  Moving average type for the slowd moving average.
            By default, slowmatype=0. Integers 0 - 8 are accepted
            (check down the mappings) or the string containing the math type can
            also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_stoch(symbol=symbol, interval=interval, fastkperiod=fastkperiod, slowkperiod=slowkperiod,
                        slowdperiod=slowdperiod, slowkmatype=slowkmatype, slowdmatype=slowdmatype, month=month,
                        entitlement=entitlement)


@mcp.tool()
def get_stochf(symbol, interval='daily', fastkperiod=None,
               fastdperiod=None, fastdmatype=None, month=None, entitlement=None):
    """ Return the stochatic oscillator values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        fastkperiod:  The time period of the fastk moving average. Positive
            integers are accepted (default=None)
        fastdperiod:  The time period of the fastd moving average. Positive
            integers are accepted (default=None)
        fastdmatype:  Moving average type for the fastdmatype moving average.
            By default, fastmatype=0. Integers 0 - 8 are accepted
            (check  down the mappings) or the string containing the math type can
            also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_stochf(symbol=symbol, interval=interval, fastkperiod=fastkperiod, fastdperiod=fastdperiod,
                         fastdmatype=fastdmatype, month=month, entitlement=entitlement)


@mcp.tool()
def get_rsi(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the relative strength index time series in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_rsi(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_stochrsi(symbol, interval='daily', time_period=20,
                 series_type='close', fastkperiod=None, fastdperiod=None,
                 fastdmatype=None, month=None, entitlement=None):
    """ Return the stochatic relative strength index in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastkperiod:  The time period of the fastk moving average. Positive
            integers are accepted (default=None)
        fastdperiod:  The time period of the fastd moving average. Positive
            integers are accepted (default=None)
        fastdmatype:  Moving average type for the fastdmatype moving average.
            By default, fastmatype=0. Integers 0 - 8 are accepted
            (check  down the mappings) or the string containing the math type can
            also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_stochrsi(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type,
                           fastkperiod=fastkperiod, fastdperiod=fastdperiod, fastdmatype=fastdmatype, month=month,
                           entitlement=entitlement)


@mcp.tool()
def get_willr(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the Williams' %R (WILLR) values in two json objects as data
    and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_willr(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_adx(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return  the average directional movement index values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_adx(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_adxr(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return  the average directional movement index  rating in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_adxr(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_apo(symbol, interval='daily', series_type='close',
            fastperiod=None, slowperiod=None, matype=None, month=None, entitlement=None):
    """ Return the absolute price oscillator values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default '60min)'
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod:  Positive integers are accepted (default=None)
        slowperiod:  Positive integers are accepted (default=None)
        matype    :  Moving average type. By default, fastmatype=0.
            Integers 0 - 8 are accepted (check  down the mappings) or the string
            containing the math type can also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_apo(symbol=symbol, interval=interval, series_type=series_type, fastperiod=fastperiod,
                      slowperiod=slowperiod, matype=matype, month=month, entitlement=entitlement)


@mcp.tool()
def get_ppo(symbol, interval='daily', series_type='close',
            fastperiod=None, slowperiod=None, matype=None, month=None, entitlement=None):
    """ Return the percentage price oscillator values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily'
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        fastperiod:  Positive integers are accepted (default=None)
        slowperiod:  Positive integers are accepted (default=None)
        matype    :  Moving average type. By default, fastmatype=0.
            Integers 0 - 8 are accepted (check  down the mappings) or the string
            containing the math type can also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ppo(symbol=symbol, interval=interval, series_type=series_type, fastperiod=fastperiod,
                      slowperiod=slowperiod, matype=matype, month=month, entitlement=entitlement)


@mcp.tool()
def get_mom(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the momentum values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_mom(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_bop(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the balance of power values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_bop(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_cci(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the commodity channel index values  in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_cci(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_cmo(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the Chande momentum oscillator in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_cmo(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_roc(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the rate of change values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_roc(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_rocr(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the rate of change ratio values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_rocr(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                       entitlement=entitlement)


@mcp.tool()
def get_aroon(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the aroon values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_aroon(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                        entitlement=entitlement)


@mcp.tool()
def get_aroonosc(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the aroon oscillator values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_aroonosc(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type,
                           month=month, entitlement=entitlement)


@mcp.tool()
def get_mfi(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the money flow index values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_mfi(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_trix(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the1-day rate of change of a triple smooth exponential
    moving average in two json objects as data and meta_data.
    It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_trix(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                       entitlement=entitlement)


@mcp.tool()
def get_ultosc(symbol, interval='daily', timeperiod1=None,
               timeperiod2=None, timeperiod3=None, month=None, entitlement=None):
    """ Return the ultimate oscillaror values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        timeperiod1:  The first time period indicator. Positive integers are
            accepted. By default, timeperiod1=7
        timeperiod2:  The first time period indicator. Positive integers are
            accepted. By default, timeperiod2=14
        timeperiod3:  The first time period indicator. Positive integers are
            accepted. By default, timeperiod3=28
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ultosc(symbol=symbol, interval=interval, timeperiod1=timeperiod1, timeperiod2=timeperiod2,
                         timeperiod3=timeperiod3, month=month, entitlement=entitlement)


@mcp.tool()
def get_dx(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the directional movement index values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_dx(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type, month=month,
                     entitlement=entitlement)


@mcp.tool()
def get_minus_di(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the minus directional indicator values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_minus_di(symbol=symbol, interval=interval, time_period=time_period, month=month,
                           entitlement=entitlement)


@mcp.tool()
def get_plus_di(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the plus directional indicator values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_plus_di(symbol=symbol, interval=interval, time_period=time_period, month=month,
                          entitlement=entitlement)


@mcp.tool()
def get_minus_dm(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the minus directional movement values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_minus_dm(symbol=symbol, interval=interval, time_period=time_period, month=month,
                           entitlement=entitlement)


@mcp.tool()
def get_plus_dm(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the plus directional movement values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_plus_dm(symbol=symbol, interval=interval, time_period=time_period, month=month,
                          entitlement=entitlement)


@mcp.tool()
def get_bbands(symbol, interval='daily', time_period=20, series_type='close',
               nbdevup=None, nbdevdn=None, matype=None, month=None, entitlement=None):
    """ Return the bollinger bands values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  Number of data points used to calculate each BBANDS value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)
            (default=20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        nbdevup:  The standard deviation multiplier of the upper band. Positive
            integers are accepted as default (default=2)
        nbdevdn:  The standard deviation multiplier of the lower band. Positive
            integers are accepted as default (default=2)
        matype :  Moving average type. By default, matype=0.
            Integers 0 - 8 are accepted (check  down the mappings) or the string
            containing the math type can also be used.

            * 0 = Simple Moving Average (SMA),
            * 1 = Exponential Moving Average (EMA),
            * 2 = Weighted Moving Average (WMA),
            * 3 = Double Exponential Moving Average (DEMA),
            * 4 = Triple Exponential Moving Average (TEMA),
            * 5 = Triangular Moving Average (TRIMA),
            * 6 = T3 Moving Average,
            * 7 = Kaufman Adaptive Moving Average (KAMA),
            * 8 = MESA Adaptive Moving Average (MAMA)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_bbands(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type,
                         nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype, month=month, entitlement=entitlement)


@mcp.tool()
def get_midpoint(symbol, interval='daily', time_period=20, series_type='close', month=None, entitlement=None):
    """ Return the midpoint values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_midpoint(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type,
                           month=month, entitlement=entitlement)


@mcp.tool()
def get_midprice(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the midprice values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_midprice(symbol=symbol, interval=interval, time_period=time_period, month=month,
                           entitlement=entitlement)


@mcp.tool()
def get_sar(symbol, interval='daily', acceleration=None, maximum=None, month=None, entitlement=None):
    """ Return the midprice values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        acceleration:  The acceleration factor. Positive floats are accepted (
            default 0.01)
        maximum:  The acceleration factor maximum value. Positive floats
            are accepted (default 0.20 )
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_sar(symbol=symbol, interval=interval, acceleration=acceleration, maximum=maximum, month=month,
                      entitlement=entitlement)


@mcp.tool()
def get_trange(symbol, interval='daily', month=None, entitlement=None):
    """ Return the true range values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_trange(symbol=symbol, interval=interval, month=month, entitlement=entitlement)


@mcp.tool()
def get_atr(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the average true range values in two json objects as
    data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_atr(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_natr(symbol, interval='daily', time_period=20, month=None, entitlement=None):
    """ Return the normalized average true range values in two json objects
    as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        time_period:  How many data points to average (default 20)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_natr(symbol=symbol, interval=interval, time_period=time_period, month=month, entitlement=entitlement)


@mcp.tool()
def get_ad(symbol, interval='daily', month=None, entitlement=None):
    """ Return the Chaikin A/D line values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ad(symbol=symbol, interval=interval, month=month, entitlement=entitlement)


@mcp.tool()
def get_adosc(symbol, interval='daily', fastperiod=None,
              slowperiod=None, month=None, entitlement=None):
    """ Return the Chaikin A/D oscillator values in two
    json objects as data and meta_data. It raises ValueError when problems
    arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily'
        fastperiod:  Positive integers are accepted (default=None)
        slowperiod:  Positive integers are accepted (default=None)
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_adosc(symbol=symbol, interval=interval, fastperiod=fastperiod, slowperiod=slowperiod, month=month,
                        entitlement=entitlement)


@mcp.tool()
def get_obv(symbol, interval='daily', month=None, entitlement=None):
    """ Return the on balance volume values in two json
    objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_obv(symbol=symbol, interval=interval, month=month, entitlement=entitlement)


@mcp.tool()
def get_ht_trendline(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, instantaneous trendline values in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_trendline(symbol=symbol, interval=interval, series_type=series_type, month=month,
                               entitlement=entitlement)


@mcp.tool()
def get_ht_sine(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, sine wave values in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
        are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_sine(symbol=symbol, interval=interval, series_type=series_type, month=month,
                          entitlement=entitlement)


@mcp.tool()
def get_ht_trendmode(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, trend vs cycle mode in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_trendmode(symbol=symbol, interval=interval, series_type=series_type, month=month,
                               entitlement=entitlement)


@mcp.tool()
def get_ht_dcperiod(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, dominant cycle period in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_dcperiod(symbol=symbol, interval=interval, series_type=series_type, month=month,
                              entitlement=entitlement)


@mcp.tool()
def get_ht_dcphase(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, dominant cycle phase in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_dcphase(symbol=symbol, interval=interval, series_type=series_type, month=month,
                             entitlement=entitlement)


@mcp.tool()
def get_ht_phasor(symbol, interval='daily', series_type='close', month=None, entitlement=None):
    """ Return the Hilbert transform, phasor components in two
    json objects as data and meta_data. It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min', 'daily',
            'weekly', 'monthly' (default 'daily')
        series_type:  The desired price type in the time series. Four types
            are supported: 'close', 'open', 'high', 'low' (default 'close')
        month:  ONLY applicable to intraday intervals.
            By default, not set and the technical indicator values will be calculated
            based on the most recent 30 days of intraday data.
        entitlement:  Supported values are 'realtime' for realtime US stock market data
            or 'delayed' for 15-minute delayed US stock market data
    """
    ti = TechIndicators(output_format='json')
    return ti.get_ht_phasor(symbol=symbol, interval=interval, series_type=series_type, month=month,
                            entitlement=entitlement)


@mcp.tool()
def get_wti(interval='monthly'):
    """ Returns the West Texas Intermediate (WTI) crude oil prices.

    Keyword Arguments:
        interval:  supported values are 'daily', 'weekly', 'monthly' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_wti(interval=interval)


@mcp.tool()
def get_brent(interval='monthly'):
    """ Returns the Brent (Europe) crude oil prices.

    Keyword Arguments:
        interval:  supported values are 'daily', 'weekly', 'monthly' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_brent(interval=interval)


@mcp.tool()
def get_natural_gas(interval='monthly'):
    """ Returns the Henry Hub natural gas spot prices.

    Keyword Arguments:
        interval:  supported values are 'daily', 'weekly', 'monthly' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_natural_gas(interval=interval)


@mcp.tool()
def get_copper(interval='monthly'):
    """ Returns the global price of copper.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_copper(interval=interval)


@mcp.tool()
def get_aluminum(interval='monthly'):
    """ Returns the global price of aluminum.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_aluminum(interval=interval)


@mcp.tool()
def get_wheat(interval='monthly'):
    """ Returns the global price of wheat.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_wheat(interval=interval)


@mcp.tool()
def get_corn(interval='monthly'):
    """ Returns the global price of corn.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_corn(interval=interval)


@mcp.tool()
def get_cotton(interval='monthly'):
    """ Returns the global price of cotton.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_cotton(interval=interval)


@mcp.tool()
def get_sugar(interval='monthly'):
    """ Returns the global price of sugar.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_sugar(interval=interval)


@mcp.tool()
def get_coffee(interval='monthly'):
    """ Returns the global price of coffee.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_coffee(interval=interval)


@mcp.tool()
def get_price_index(interval='monthly'):
    """ Returns the global price index of all commodities.

    Keyword Arguments:
        interval:  supported values are 'monthly', 'quarterly', 'annual' (default 'monthly')
    """
    cm = Commodities(output_format='json')
    return cm.get_price_index(interval=interval)


@mcp.tool()
def get_currency_exchange_rate(from_currency, to_currency):
    """ Returns the realtime exchange rate for any pair of physical
    currency (e.g., EUR) or physical currency (e.g., USD).

    Keyword Arguments:
        from_currency: The currency you would like to get the exchange rate
        for. It can either be a physical currency or digital/crypto currency.
        For example: from_currency=USD or from_currency=BTC.
        to_currency: The destination currency for the exchange rate.
        It can either be a physical currency or digital/crypto currency.
        For example: to_currency=USD or to_currency=BTC.
    """
    fg = ForeignExchange(output_format='json')
    return fg.get_currency_exchange_rate(from_currency, to_currency)


@mcp.tool()
def get_currency_exchange_intraday(from_symbol, to_symbol, interval='15min', outputsize='compact'):
    """ Returns the intraday exchange rate for any pair of physical
    currency (e.g., EUR) or physical currency (e.g., USD).

    Keyword Arguments:
        from_symbol: The currency you would like to get the exchange rate
            for.
            For example: from_currency=EUR or from_currency=USD.
        to_symbol: The destination currency for the exchange rate.
            For example: to_currency=USD or to_currency=JPY.
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min'
            (default '15min')
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length intraday times
            series, commonly above 1MB (default 'compact')
    """
    fg = ForeignExchange(output_format='json')
    return fg.get_currency_exchange_intraday(from_symbol, to_symbol, interval=interval, outputsize=outputsize)


@mcp.tool()
def get_currency_exchange_daily(from_symbol, to_symbol, outputsize='compact'):
    """ Returns the daily exchange rate for any pair of physical
    currency (e.g., EUR) or physical currency (e.g., USD).

    Keyword Arguments:
        from_symbol: The currency you would like to get the exchange rate
            for.
            For example: from_symbol=EUR or from_symbol=USD.
        to_symbol: The destination currency for the exchange rate.
            For example: to_symbol=USD or to_symbol=JPY.
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length daily times
            series, commonly above 1MB (default 'compact')
    """
    fg = ForeignExchange(output_format='json')
    return fg.get_currency_exchange_daily(from_symbol, to_symbol, outputsize=outputsize)


@mcp.tool()
def get_currency_exchange_weekly(from_symbol, to_symbol, outputsize='compact'):
    """ Returns the weekly exchange rate for any pair of physical
    currency (e.g., EUR) or physical currency (e.g., USD).

    Keyword Arguments:
        from_symbol: The currency you would like to get the exchange rate
            for.
            For example: from_symbol=EUR or from_symbol=USD.
        to_symbol: The destination currency for the exchange rate.
            For example: to_symbol=USD or to_symbol=JPY.
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length weekly times
            series, commonly above 1MB (default 'compact')
    """
    fg = ForeignExchange(output_format='json')
    return fg.get_currency_exchange_weekly(from_symbol, to_symbol, outputsize=outputsize)


@mcp.tool()
def get_currency_exchange_monthly(from_symbol, to_symbol, outputsize='compact'):
    """ Returns the monthly exchange rate for any pair of physical
    currency (e.g., EUR) or physical currency (e.g., USD).

    Keyword Arguments:
        from_symbol: The currency you would like to get the exchange rate
            for.
            For example: from_symbol=EUR or from_symbol=USD.
        to_symbol: The destination currency for the exchange rate.
            For example: to_symbol=USD or to_symbol=JPY.
        interval:  time interval between two conscutive values,
            supported values are '1min', '5min', '15min', '30min', '60min'
            (default '15min')
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length monthly times
            series, commonly above 1MB (default 'compact')
    """
    fg = ForeignExchange(output_format='json')
    return fg.get_currency_exchange_monthly(from_symbol, to_symbol, outputsize=outputsize)


# @mcp.tool()
# def get_real_gdp(interval='annual'):
#     """ Returns the annual and quarterly Real GDP of the United States

#     Keyword Arguments:
#         interval:  supported values are 'quarterly', 'annual' (default 'annual')
#     """
#     ei = EconIndicators(output_format='json')
#     return ei.get_real_gdp(interval=interval)
@mcp.tool()
def get_real_gdp(interval='annual'):
    """
    Get Real GDP data and save to file
    """
    ei = EconIndicators(output_format='json')
    data = ei.get_real_gdp(interval=interval)
    
    # Save data to file
    import json
    from datetime import datetime
    
    filename = f"gdp_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return data


@mcp.tool()
def get_real_gdp_per_capita(interval='annual'):
    """ Returns the quarterly Real GDP per Capita data of the United States
    """
    ei = EconIndicators(output_format='json')
    return ei.get_real_gdp_per_capita(interval=interval)


@mcp.tool()
def get_treasury_yield(interval='monthly', maturity='10year'):
    """ Returns the US treasury yield of a given maturity timeline

    Keyword Arguments:
        interval:  supported values are 'daily', 'weekly', 'monthly' (default 'monthly')
        maturity:  supported values are '3month', '2year', '5year', '7year',
            '10year', '30year' (default '10year')
    """
    ei = EconIndicators(output_format='json')
    return ei.get_treasury_yield(interval=interval, maturity=maturity)


@mcp.tool()
def get_ffr(interval='monthly'):
    """ Returns the federal funds rate (interest rate) of the United States

    Keyword Arguments:
        interval:  supported values are 'daily', 'weekly', 'monthly' (default 'monthly')
    """
    ei = EconIndicators(output_format='json')
    return ei.get_ffr(interval=interval)


@mcp.tool()
def get_cpi(interval='monthly'):
    """ Returns the consumer price index of the United States

    Keyword Arguments:
        interval:  supported values are 'semiannual', 'monthly' (default 'monthly')
    """
    ei = EconIndicators(output_format='json')
    return ei.get_cpi(interval=interval)


@mcp.tool()
def get_inflation():
    """ Returns the annual inflation rates (consumer prices) of the United States
    """
    ei = EconIndicators(output_format='json')
    return ei.get_inflation()


@mcp.tool()
def get_retail_sales():
    """ Returns the monthly Advance Retail Sales: Retail Trade data of the United States
    """
    ei = EconIndicators(output_format='json')
    return ei.get_retail_sales()


@mcp.tool()
def get_durables():
    """ Returns the monthly manufacturers' new orders of durable goods in the United States
    """
    ei = EconIndicators(output_format='json')
    return ei.get_durables()


@mcp.tool()
def get_unemployment():
    """ Returns the monthly unemployment data of the United States
    """
    ei = EconIndicators(output_format='json')
    return ei.get_unemployment()


@mcp.tool()
def get_nonfarm():
    """ Returns the monthly US All Employees: Total Nonfarm
    """
    ei = EconIndicators(output_format='json')
    return ei.get_nonfarm()


@mcp.tool()
def get_news_sentiment(tickers=None, topics=None, time_from=None, time_to=None,
                       sort='LATEST', limit=50):
    """ Return live and historical market news & sentiment data
    from news outlets around the world.
    It raises ValueError when problems arise

    Keyword Arguments:
        tickers:  the stock/crypto/forex symbols of your choice
        topics:  news topics of your choice
        time_from and time_to:  time range of the news articles you are targeting,
            in YYYYMMDDTHHMM format. If time_from is specified but time_to is missing,
            returns articles published between the time_from value and the current time
        sort:  sort articles returned by API
            supported values are 'LATEST', 'EARLIEST', 'RELEVANCE' (default 'LATEST')
        limit:  number of output results
            supported values are 50, 1000 (default 50)
    """
    ai = AlphaIntelligence(output_format='json')
    return ai.get_news_sentiment(tickers=tickers, topics=topics, time_from=time_from, time_to=time_to, sort=sort,
                                 limit=limit)


@mcp.tool()
def get_top_gainers():
    """ Returns the top 20 gainers in the US market.
    It raises ValueError when problems arise.
    """
    ai = AlphaIntelligence(output_format='json')
    return ai.get_top_gainers()


@mcp.tool()
def get_top_losers(self):
    """ Returns the top 20 losers in the US market.
    It raises ValueError when problems arise.
    """
    ai = AlphaIntelligence(output_format='json')
    return ai.get_top_losers()


@mcp.tool()
def get_most_active():
    """ Returns the top 20  most actively traded tickers in the US market.
    It raises ValueError when problems arise.
    """
    ai = AlphaIntelligence(output_format='json')
    return ai.get_most_active()


@mcp.tool()
def get_realtime_options(symbol, contract=None):
    """ Return realtime US options data.
    It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        contract:  US options contract ID.
            By default, not set and entire option chain is returned
    """
    optoions = Options(output_format='json')
    return optoions.get_realtime_options(symbol=symbol, contract=contract)


@mcp.tool()
def get_historical_options(symbol, date=None):
    """ Return historical US options data.
    It raises ValueError when problems arise

    Keyword Arguments:
        symbol:  the symbol for the equity we want to get its data
        date:  By default, not set and data for the previous trading session is returned.
            Any date later than 2008-01-01 is accepted.
    """
    optoions = Options(output_format='json')
    return optoions.get_historical_options(symbol=symbol, date=date)


@mcp.tool()
def get_digital_currency_daily(symbol, market):
    """ Returns  the daily historical time series for a digital currency
    (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan),
    refreshed daily at midnight (UTC). Prices and volumes are quoted in
    both the market-specific currency and USD..

    Keyword Arguments:
        symbol: The digital/crypto currency of your choice. It can be any
        of the currencies in the digital currency list. For example:
        symbol=BTC.
        market: The exchange market of your choice. It can be any of the
        market in the market list. For example: market=CNY.
    """
    cc = CryptoCurrencies(output_format='json')
    return cc.get_digital_currency_daily(symbol=symbol, market=market)


@mcp.tool()
def get_digital_currency_weekly(symbol, market):
    """ Returns  the weekly historical time series for a digital currency
    (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan),
    refreshed daily at midnight (UTC). Prices and volumes are quoted in
    both the market-specific currency and USD..

    Keyword Arguments:
        symbol: The digital/crypto currency of your choice. It can be any
        of the currencies in the digital currency list. For example:
        symbol=BTC.
        market: The exchange market of your choice. It can be any of the
        market in the market list. For example: market=CNY.
    """
    cc = CryptoCurrencies(output_format='json')
    return cc.get_digital_currency_weekly(symbol=symbol, market=market)


@mcp.tool()
def get_digital_currency_monthly(symbol, market):
    """ Returns  the monthly historical time series for a digital currency
    (e.g., BTC) traded on a specific market (e.g., CNY/Chinese Yuan),
    refreshed daily at midnight (UTC). Prices and volumes are quoted in
    both the market-specific currency and USD..

    Keyword Arguments:
        symbol: The digital/crypto currency of your choice. It can be any
        of the currencies in the digital currency list. For example:
        symbol=BTC.
        market: The exchange market of your choice. It can be any of the
        market in the market list. For example: market=CNY.
    """
    cc = CryptoCurrencies(output_format='json')
    return cc.get_digital_currency_monthly(symbol=symbol, market=market)


@mcp.tool()
def get_digital_currency_exchange_rate(from_currency, to_currency):
    """ Returns the realtime exchange rate for any pair of digital
    currency (e.g., BTC) or physical currency (e.g., USD).
    Keyword Arguments:
        from_currency: The currency you would like to get the exchange rate
        for. It can either be a physical currency or digital/crypto currency.
        For example: from_currency=USD or from_currency=BTC.
        to_currency: The destination currency for the exchange rate.
        It can either be a physical currency or digital/crypto currency.
        For example: to_currency=USD or to_currency=BTC.
    """
    cc = CryptoCurrencies(output_format='json')
    return cc.get_digital_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)


@mcp.tool()
def get_crypto_intraday(symbol, market, interval, outputsize='compact'):
    """ Returns the intraday time series
    of the cryptocurrency specified, updated realtime.

    Keyword Arguments:
        symbol:  digital/crypto currency of your choice
        market:  exchange market of your choice
        interval:  time interval between two consecutive values,
            supported values are '1min', '5min', '15min', '30min', '60min'
        outputsize:  The size of the call, supported values are
            'compact' and 'full; the first returns the last 100 points in the
            data series, and 'full' returns the full-length intraday times
            series (default 'compact')
    """
    cc = CryptoCurrencies(output_format='json')
    return cc.get_crypto_intraday(symbol=symbol, market=market, interval=interval, outputsize=outputsize)


if __name__ == "__main__":
    mcp.run(transport='stdio')
