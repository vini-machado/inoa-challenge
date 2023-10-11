from datetime import datetime
from django.db import models

class Stock(models.Model):
    """
    Represents a stock or equity in the system.

    Attributes:
        ticker (str): The stock's ticker symbol, a short identifier.
            Max length is 5 characters.
        interval (str): The interval at which data is collected for this stock.
            Max length is 4 characters.
    """

    ticker   = models.CharField(max_length=5)
    interval = models.CharField(max_length=4)

class StockData(models.Model):
    """
    Represents historical data for a specific stock.

    Attributes:
        stock (Stock): The associated stock for which this data is recorded.
        date_time (DateTimeField): The date and time when this data was recorded.
            Defaults to the current datetime if not specified.
        open_price (DecimalField): The opening price of the stock on the recorded date.
            Max digits: 3, Decimal places: 2, Default: 0.
        close_price (DecimalField): The closing price of the stock on the recorded date.
            Max digits: 3, Decimal places: 2, Default: 0.
        high_price (DecimalField): The highest price of the stock on the recorded date.
            Max digits: 3, Decimal places: 2, Default: 0.
        low_price (DecimalField): The lowest price of the stock on the recorded date.
            Max digits: 3, Decimal places: 2, Default: 0.
        volume (IntegerField): The trading volume for the stock on the recorded date.
            Default: 0.
    """
    stock       = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_time   = models.DateTimeField(default=datetime.now)
    open_price  = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    close_price = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    high_price  = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    low_price   = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    volume      = models.IntegerField(default=0)
