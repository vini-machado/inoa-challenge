from typing import Any
from django.shortcuts import render
from django.views import View
import pandas as pd
from ..utils.stock_handler import StockHandler
from ..utils.stock_chart import StockChart



class StockDataView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
        self.template_name = 'stock_data.html'
        self.sh = StockHandler()
        self.context = dict()

    def get(self, request, ticker: str, interval: str):
        self.__define_context(ticker, interval)

        return render(request, self.template_name , self.context)
    

    ############################### CONTEXT ##################################
    def __define_context(self, ticker: str, interval: str):
        raw_data, table_data = self.__handle_stock_data(ticker, interval)

        self.context['plot']       = self.__plot_context(raw_data)
        self.context['ticker']     = ticker
        self.context['stock_data'] = table_data
    
    def __plot_context(self, data: pd.DataFrame):
        plot_data  = data.reset_index()

        sc   = StockChart(plot_data)
        plot = sc.plot()

        return plot
    ############################### CONTEXT ##################################
         
    
    ############################### HELPERS ##################################
    def __handle_stock_data(self, ticker: str, interval: str) -> tuple[pd.DataFrame, list[dict]]:
        raw_data = self.sh.get_stock_data(ticker, interval)
        
        stock_data = self.__modify_raw_data(raw_data.copy())
        stock_data = stock_data.to_dict('records')

        return raw_data, stock_data

    def __modify_raw_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        if 'Datetime' in raw_data.columns:
            raw_data['Datetime'] = raw_data['Datetime'].dt.strftime("%d/%m/%Y - %Hh%M")
        else:
            raw_data['Datetime'] = raw_data['Date'].dt.strftime("%d/%m/%Y")

        raw_data['Volume']   = raw_data['Volume']/1000

        raw_data = raw_data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        raw_data = raw_data[::-1]


        return raw_data