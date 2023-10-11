from datetime import datetime
import itertools
import pandas as pd
import yfinance as yf

from stock_fetcher import INTERVALS, STOCK_LIST_FILE
from stock_fetcher.models import Stock

class StockHandler:
    def __init__(self) -> None:
        self.__initialize_stock_model()

    def __initialize_stock_model(self) -> None:
        """
        Initialize the Stock model by creating database records for all combinations of ticker symbols and intervals.
        Returns:
            None

        Note:
        - This function is meant for initializing the Stock model and should be called
        when setting up the application or when stock data tracking needs to be initiated.
        - Existing records in the Stock model will not be modified, and new records will
        be created.
        """
        ticker_symbols   = self.__get_all_tickers()
        ticker_intervals = self.__cross_product_tickers_intervals(ticker_symbols)

        for ticker, interval in ticker_intervals:
            s = Stock(ticker = ticker, interval = interval)
            s.save()

    def __get_all_tickers(self) -> list[str]:
        """
        Retrieve a list of stock ticker symbols from a file and format them.

        Reads stock ticker symbols from a file specified by the constant
        STOCK_LIST_FILE, one symbol per line, and appends ".SA" to each symbol.

        Returns:
            list[str]: A list of formatted stock ticker symbols.

        This function is intended to be used for internal purposes and should not
        be directly called outside the class.
        """

        with open(STOCK_LIST_FILE, 'r') as ticker_file:
            ticker_symbols = ticker_file.readlines()

            ticker_symbols = [ticker.replace("\n", "") + ".SA" for ticker in ticker_symbols]
            return ticker_symbols
        
    def __cross_product_tickers_intervals(self, ticker_symbols: list[str]) -> tuple[str, str]:
        """
        Generate a cross-product of stock ticker symbols and time intervals.

        Args:
            ticker_symbols (list[str]): A list of stock ticker symbols to combine.
        
        Returns:
            tuple[str, str]: A tuple of cross-product combinations containing stock ticker
            symbols and predefined time intervals.

        This function is intended for internal use and should not be directly called
        outside the class.

        """
        return tuple(itertools.product(ticker_symbols, INTERVALS))
        
    def get_stock_data(self, ticker_symbol: str, interval: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Retrieve historical stock data for a specific symbol within a date range.

        Args:
            ticker_symbol (str): The stock ticker symbol for which to fetch data.
            interval (str): The time interval for data collection (e.g., '1d' for daily).
            start_date (datetime): The start date for data retrieval.
            end_date (datetime): The end date for data retrieval.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing historical stock data.

        This function uses the yfinance library to fetch historical stock data for the
        specified ticker symbol. The data is collected within the given date range and
        at the specified time interval. The resulting data is returned as a Pandas DataFrame.

        """
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval, progress=False)

        return stock_data
