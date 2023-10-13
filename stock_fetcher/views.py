from django.shortcuts import render
from django.views import View
from .models import Stock
from django.http import JsonResponse

class StocksView(View):
    TEMPLATE_NAME= 'all_stocks.html'
    
    def get(self, request):
        stocks = Stock.objects.all()
        
        context = {
            'stocks': stocks,
        }
        
        return render(request, self.TEMPLATE_NAME, context)


class StockDataView(View):
    TEMPLATE_NAME= 'stock_data.html'
    def get(self, request, ticker, interval):
        stock_data = self.__stock_data_to_list_of_dicts(ticker, interval)
        
        context = {
            'stock_data': stock_data,
        }

        return render(request, self.TEMPLATE_NAME, context)
    
    def __stock_data_to_list_of_dicts(self, ticker: str, interval: str):
        from .utils.stock_handler import StockHandler

        sh = StockHandler()
        stock_data = sh.get_stock_data(ticker, interval)

        stock_data['Datetime'] = stock_data['Datetime'].dt.strftime("%d/%m/%Y - %Hh%M")
        stock_data['Volume']   = stock_data['Volume']/1000

        stock_data = stock_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        stock_data = stock_data[::-1]
        return stock_data.to_dict('records')
