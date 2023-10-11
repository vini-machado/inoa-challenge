from django.shortcuts import render
from django.views import View
from .models import Stock

def stock_data(request):
    stocks = Stock.objects.all()  # Fetch all Stock records
    
    context = {
        'stocks': stocks,
    }
    
    return render(request, "stock_data.html", context)