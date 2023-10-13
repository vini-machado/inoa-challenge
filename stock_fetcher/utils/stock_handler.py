from datetime import datetime
import itertools
import pandas as pd
import yfinance as yf
from tqdm import tqdm

from stock_fetcher import INTERVALS, STOCK_LIST_FILE
from stock_fetcher.models import Stock

class StockHandler:
    def __init__(self) -> None:
        self.ticker_symbols = self.__get_all_tickers()

        if len(Stock.objects.all()) == 0:
            self.get_current_prices()

    def get_current_prices(self) -> None:
        """
        Retrieves the current prices for a list of ticker symbols and updates the database accordingly.

        This function iterates through a list of ticker symbols and obtains the current price for each symbol.
        It then calls the private method __get_current_price to fetch the current price for each ticker symbol.
        Subsequently, it utilizes the Stock.create_or_update method to either create a new record or update an existing one 
        in the database with the obtained ticker symbol and its current price.

        Returns:
        None. This function does not return any value.

        Raises:
        Any exceptions that occur during the process of fetching or updating prices may be raised and left unhandled.
        """
        for ticker in tqdm(self.ticker_symbols):
            current_price = self.__get_current_price(ticker)
            
            Stock.create_or_update(ticker = ticker, current_price = current_price)

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
        
    def __get_current_price(self, ticker):
        return yf.Ticker(ticker).info.get('currentPrice')
   
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