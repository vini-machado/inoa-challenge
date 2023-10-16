from django.db import models
from django.contrib.auth.models import User
from stock_fetcher.models import Stock

class UserStock(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    max_price = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    min_price = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    periodicity = models.CharField(max_length=3, null=True, default = '5m')

    @classmethod
    def create_or_update(self, user, stock, max_price = 0, min_price = 0, periodicity = None):
        defaults = {
            'max_price' : max_price,
            'min_price' : min_price,
            'periodicity' : periodicity
        }

        obj, created = self.objects.get_or_create(user=user, stock=stock, defaults=defaults)
        if not created:
            obj.max_price = defaults.get('max_price')
            obj.min_price = defaults.get('min_price')
            obj.periodicity = defaults.get('periodicity')
            
            obj.save()