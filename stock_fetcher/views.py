from django.shortcuts import render
from django.views import View
import pandas as pd
from .models import Stock
from .utils.stock_chart import StockChart
from .utils.stock_handler import StockHandler

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
    sh = StockHandler()

    def get(self, request, ticker, interval):
        raw_data = self.sh.get_stock_data(ticker, interval)
        
        plot_data  = raw_data.reset_index()
        sc   = StockChart(plot_data)
        plot = sc.plot()
         
        stock_data = self.__stock_data_to_list_of_dicts(raw_data)
        
        context = {
            'ticker' : ticker,
            'stock_data': stock_data,
            'plot': plot
        }

        return render(request, self.TEMPLATE_NAME, context)
    
    def __stock_data_to_list_of_dicts(self, raw_data: pd.DataFrame) -> list[dict]:
        stock_data = self.__modify_raw_data(raw_data)
        
        return stock_data.to_dict('records')

    def __modify_raw_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        if 'Datetime' in raw_data.columns:
            raw_data['Datetime'] = raw_data['Datetime'].dt.strftime("%d/%m/%Y - %Hh%M")
        else:
            raw_data['Datetime'] = raw_data['Date'].dt.strftime("%d/%m/%Y")

        raw_data['Volume']   = raw_data['Volume']/1000

        raw_data = raw_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        raw_data = raw_data[::-1]


        return raw_data
