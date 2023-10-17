from ..models import UserStock
from stock_fetcher.models import Stock

class PeriodTickers:
    def __init__(self) -> None:
        self.user_stocks   = UserStock

    def __stock_periodicity_set(self):
        return self.user_stocks.objects.values('stock', 'periodicity').distinct()
    
    def __set_to_periodicity_dict(self) -> dict[str, list[int]]:
        sp_set = self.__stock_periodicity_set()
        monitoring_periods = dict()

        for item in sp_set:
            stock       = item['stock']
            periodicity = item['periodicity']

            if periodicity in monitoring_periods:
                monitoring_periods[periodicity].append(stock)
            else:
                monitoring_periods[periodicity] = [stock]
        return monitoring_periods # {'5m': [1, 2, 3], '15m': [3, 4, 5]}
    
    def __transform_stock_id_to_ticker(self) -> dict[str, list[str]]:
        monitoring_periods = self.__set_to_periodicity_dict()
        stocks = lambda period: Stock.objects.filter(id__in = monitoring_periods[period]).values_list('ticker', flat=True)

        for period in monitoring_periods.keys():
            monitoring_periods[period] = list(stocks(period))
        return monitoring_periods # {'5m': ['MGLU3.SA', 'VALE3.SA'], '15m': ['PETR3.SA']}
    
    @property
    def to_monitoring(self) -> dict[str, list[str]]:
        return self.__transform_stock_id_to_ticker()