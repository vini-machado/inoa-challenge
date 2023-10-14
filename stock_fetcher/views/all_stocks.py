from typing import Any
from django.shortcuts import render
from django.views import View
import pandas as pd
from ..models import Stock
from ..utils.stock_handler import StockHandler

class StocksView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = 'all_stocks.html'
        self.stocks = Stock.objects.all()
        self.context = dict()

    def get(self, request):
        self.__define_context()

        return render(request, self.template_name, self.context)



    def __define_context(self):
        self.context['stocks'] = self.stocks
