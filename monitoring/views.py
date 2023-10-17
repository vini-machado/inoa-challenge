from .models import UserStock
from .utils.period_tickers import PeriodTickers
from .utils.tunnel_price  import TunnelPrice
from .utils.email_handler  import Email
from stock_fetcher.models import Stock
from stock_fetcher.utils.stock_handler import StockHandler
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
class Monitoring:
    def __init__(self) -> None:
        self.stock_handler = StockHandler()
        self.scheduler = BackgroundScheduler()
    
    @property
    def period_tickers(self):
        return PeriodTickers().to_monitoring
    
    @property
    def period_minutes(self):
        return {
            period: int(period.split('m')[0]) for period in self.period_tickers.keys()
            }

    def ticker_high_low_prices(self, periodicity: str, ticker_list: list[str]) -> pd.DataFrame:
        return self.stock_handler.get_tickers_high_low_prices(periodicity, ticker_list)
    
    def execute(self):
        for periodicity, tickers in self.period_tickers.items():
            minutes = self.period_minutes[periodicity]

            self.scheduler.add_job(self.check_tunnel, args = [periodicity, tickers], trigger = 'interval', minutes = minutes, max_instances = 2)
            self.scheduler.start()

    def check_tunnel(self, periodicity: str, ticker_list: list[str]):
        current_high_low = self.ticker_high_low_prices(periodicity, ticker_list)
        tunnel_price = TunnelPrice(current_high_low)

        print(tunnel_price.tunnel_data)
        Email(tunnel_price).send()

