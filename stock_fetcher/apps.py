from django.apps import AppConfig


class StockFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_fetcher'

    def ready(self) -> None:
        from .utils.stock_handler import StockHandler
        
        StockHandler()