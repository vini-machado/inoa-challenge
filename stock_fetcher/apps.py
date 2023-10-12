from django.apps import AppConfig
import sys


class StockFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_fetcher'

    def ready(self) -> None:
        if 'runserver' in sys.argv:
            from .utils.stock_handler import StockHandler
            
            StockHandler()