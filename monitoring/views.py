from .models import UserStock
from .utils.period_tickers import PeriodTickers
from .utils.tunnel_price  import TunnelPrice
from .utils.email_handler  import Email
from stock_fetcher.models import Stock
from stock_fetcher.utils.stock_handler import StockHandler
import pandas as pd
import time 

INTERVALS = {
        1 : '1m', 5: '5m',
        15: '15m', 30: '30m',
        60: '60m' 
}
class Monitoring:
    def __init__(self) -> None:
        self.stock_handler = StockHandler()
        self.__update_period_tickers()

    def __update_period_tickers(self):
        self.period_tickers = PeriodTickers().to_monitoring
    
    @property
    def period_minutes(self):
        return {
            period: int(period.split('m')[0]) for period in self.period_tickers.keys()
            }

    def ticker_high_low_prices(self, periodicity: str, ticker_list: list[str]):
        return self.stock_handler.get_tickers_high_low_prices(periodicity, ticker_list)
    

    def tunnel_actions(self, periodicity: str, ticker_list: list[str]) -> pd.DataFrame:
        current_high_low = self.ticker_high_low_prices(periodicity, ticker_list)

        return TunnelPrice(current_high_low).actions
    
    def send_email(self, periodicity: str, ticker_list: list[str]):
        tunnel_actions = self.tunnel_actions(periodicity, ticker_list)
        Email(tunnel_actions).send()

    def run(self, minutes: int):
        periodicity = INTERVALS[minutes]

        self.__update_period_tickers()
        ticker_list = self.period_tickers.get(periodicity)
        
        if ticker_list is None:
            return 

        self.send_email(periodicity, ticker_list)

    def execute(self, scheduler):
        for minutes in INTERVALS.keys():

            scheduler.add_job(self.run, args = [minutes], trigger = 'interval', minutes = minutes, max_instances = 2)

        scheduler.start()