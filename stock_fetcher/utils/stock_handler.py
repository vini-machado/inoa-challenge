from datetime import datetime
import itertools
import pandas as pd
import yahooquery as yq
import investpy as inv
import numpy as np

from stock_fetcher import INTERVALS, DELISTED_TICKERS
from stock_fetcher.models import Stock

class StockHandler:
    def __init__(self, ticker_symbols = None) -> None:
        if ticker_symbols:
            self.ticker_symbols = ticker_symbols
        else:
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

        tickers_current_prices = self.__get_tickers_current_price()

        for ticker, current_price in tickers_current_prices:
            Stock.create_or_update(ticker = ticker, current_price = current_price)


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
        data = yq.Ticker(self.ticker_symbols, asynchronous = True).history(period="1d", interval="1m").reset_index()
        data = self.__format_yq_dataframe(data)

        current_price = data.groupby('Ticker').last()['Close'].to_frame().reset_index()

        return list(current_price.itertuples(index=False, name=None))
    
    
    def get_tickers_high_low_prices(self, periodicity: str, ticker_list: list[str]) -> pd.DataFrame:
        data = yq.Ticker(ticker_list, asynchronous = True).history(period="1d", interval=periodicity).reset_index()
        data = self.__format_yq_dataframe(data)

        sorted_data = data.sort_values(by='Datetime', ascending=False)

        # Keep only the first row for each 'Ticker'
        most_recent_data = sorted_data.groupby('Ticker').first().reset_index()
        return most_recent_data[['Ticker', 'High', 'Low']]

    def get_stock_data(self, ticker: str, interval: str = '1m', period: str = '5d') -> pd.DataFrame:
        data = yq.Ticker(ticker).history(interval = interval, period = period).reset_index()
        data = self.__format_yq_dataframe(data)

        return data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
    

    def __format_yq_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.round(2)
        df.rename({
            
            'symbol': 'Ticker',
            'date': 'Datetime',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close'	: 'Close',
            'volume': 'Volume',
        }, axis = 1, inplace = True)

        return df