from datetime import datetime
import itertools
import pandas as pd
import yfinance as yf
import investpy as inv
import numpy as np

from stock_fetcher import INTERVALS, DELISTED_TICKERS
from stock_fetcher.models import Stock

class StockHandler:
    def __init__(self) -> None:
        self.ticker_symbols = self.__get_all_tickers()

        if len(Stock.objects.all()) == 0:
            self.__get_current_prices()

    def __get_current_prices(self) -> None:
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

        tickers_current_prices = self.__get_tickers_current_price()

        for ticker, current_price in tickers_current_prices:
            Stock.create_or_update(ticker = ticker, current_price = current_price)

    def scheduled_functions(self):
        self.__get_current_prices()

    def __get_all_tickers(self) -> list[str]:
        """
        Retrieves a list of stock tickers from the Brazilian market and processes them.

        This private method utilizes the 'investpy' library to fetch a list of stock tickers from the Brazilian market.
        It then filters out any tickers that are present in the DELISTED_TICKERS list, and processes the remaining tickers
        by appending the ".SA" suffix to each ticker symbol.

        Returns:
        list[str]: A list of processed stock tickers from the Brazilian market with the ".SA" suffix.

        Note:
        This function requires the 'investpy' library to be installed.

        Raises:
        Any exceptions that occur during the process of fetching or processing the stock tickers may be raised and left unhandled.
        """
        all_tickers = inv.stocks.get_stocks_list(country = 'brazil')
        listed_tickers = [ticker for ticker in all_tickers if ticker not in DELISTED_TICKERS]

        ticker_symbols = [ticker.replace("\n", "") + ".SA" for ticker in listed_tickers]
        return ticker_symbols
    
    def __get_tickers_current_price(self)-> list[tuple[str, float]]:
        tickers_data = self.get_stock_data()
        unstacked_data = tickers_data.unstack()

        def current_price(ticker):
            price = unstacked_data[ticker]['Close'].iloc[-1]
            return 0 if np.isnan(price) else price
        
        return [(ticker, current_price(ticker)) for ticker in self.ticker_symbols] 
   
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
        
    def get_stock_data(self, interval: str = '1m', period: str = '1d') -> pd.DataFrame:
        """
        Retrieves historical stock data for a list of ticker symbols.

        This function utilizes the yfinance library to retrieve historical stock data for a specified list of ticker symbols.
        It allows customization of the time interval and the period for which the data is fetched. By default, it fetches data
        at 1-minute intervals for a 1-day period.

        Args:
        self: The instance of the class.
        interval (str): The time interval at which data is fetched. Default is '1m' (1 minute).
        period (str): The period for which data is fetched. Default is '1d' (1 day).

        Returns:
        pd.DataFrame: A Pandas DataFrame containing the historical stock data for the specified ticker symbols.

        Note:
        This function requires the yfinance library to be installed.

        Raises:
        Any exceptions that occur during the process of fetching the stock data may be raised and left unhandled.
        """
        stock_data = yf.Tickers(self.ticker_symbols).history(interval=interval, period = period, progress=False, group_by = 'ticker', rounding=True)

        return stock_data
