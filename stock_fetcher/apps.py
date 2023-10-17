from django.apps import AppConfig
import sys


class StockFetcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock_fetcher'