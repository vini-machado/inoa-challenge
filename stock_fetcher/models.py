from datetime import datetime
from django.db import models

class Stock(models.Model):
    """
    Represents a stock or equity in the system.

    Attributes:
        ticker (str): The stock's ticker symbol, a short identifier.
            Max length is 5 characters.
        current_price (DecimalField): The current price of the stock.
            Max digits: 5, Decimal places: 2, Default: 0.
    """

    ticker        = models.CharField(max_length=7, unique=True)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        ordering = ['ticker']

    def __str__(self):
        return self.ticker

    @classmethod
    def create_or_update(self, ticker, current_price):
        """
        Create a new object if it doesn't exist or update an existing object.

        This method attempts to retrieve an object with the specified 'ticker'.
        If such an object exists, it updates the 'current_price' with the provided value.
        If no object with the 'ticker' is found, it creates a new object with the
        specified 'ticker' and 'current_price'.

        Args:
            ticker (str): The unique ticker symbol to search for or create.
            current_price (Decimal): The updated or initial current price for the ticker.

        Returns:
            YourModel: The created or updated instance of the model.
        """
        obj, created = self.objects.get_or_create(ticker=ticker, defaults={'current_price': current_price})
        if not created:
            obj.current_price = current_price
            obj.save()

class StockData(models.Model):
    """
    Represents historical data for a specific stock.

    Attributes:
        stock (Stock): The associated stock for which this data is recorded.
        date_time (DateTimeField): The date and time when this data was recorded.
            Defaults to the current datetime if not specified.
        open_price (DecimalField): The opening price of the stock on the recorded date.
            Max digits: 5, Decimal places: 2, Default: 0.
        close_price (DecimalField): The closing price of the stock on the recorded date.
            Max digits: 5, Decimal places: 2, Default: 0.
        high_price (DecimalField): The highest price of the stock on the recorded date.
            Max digits: 5, Decimal places: 2, Default: 0.
        low_price (DecimalField): The lowest price of the stock on the recorded date.
            Max digits: 5, Decimal places: 2, Default: 0.
        volume (IntegerField): The trading volume for the stock on the recorded date.
            Default: 0.
    """
    stock       = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date_time   = models.DateTimeField(default=datetime.now)
    open_price  = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    close_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    high_price  = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    low_price   = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    volume      = models.IntegerField(default=0)
