import threading  
import time
from apscheduler.schedulers.background import BackgroundScheduler

from .stock_handler import StockHandler

class StockScheduler:
    def __init__(self) -> None:
        self.stock_handler = StockHandler()

    def start(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.stock_handler.scheduled_functions, 'interval', minutes=2, max_instances = 2)
        scheduler.start()