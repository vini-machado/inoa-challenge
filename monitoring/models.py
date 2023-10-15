from django.db import models
from django.contrib.auth.models import User
from stock_fetcher.models import Stock

class UserStock(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    max_price = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    min_price = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    periodicity = models.CharField(max_length=3, null=True)