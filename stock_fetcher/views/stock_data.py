from typing import Any
from django.shortcuts import render
from django.views import View
from django import forms
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import pandas as pd
from ..utils.stock_handler import StockHandler
from ..utils.stock_chart import StockChart
from stock_fetcher import INTERVALS, PERIODS

class TimeForm(forms.Form):
    interval = forms.ChoiceField(choices = INTERVALS,
                                       widget=forms.Select(attrs={'class': 'form-select'}),
                                       label="Select Time Interval")

    period   = forms.ChoiceField(choices = PERIODS,
                                    widget=forms.Select(attrs={'class': 'form-select'}),
                                    label="Select Time Period")

class StockDataView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = 'stock_data.html'
        self.sh = StockHandler()
        self.context = dict()

    @method_decorator(cache_page(60 * 5))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, ticker: str):
        interval = request.GET.get('interval')
        period   = request.GET.get('period')
        
        self.__define_context(request, ticker, interval, period)

        return render(request, self.template_name , self.context)
        
    ############################### GET CONTEXT ##################################
    def __define_context(self, request, ticker: str, interval: str, period: str):
        raw_data, table_data = self.__handle_stock_data(ticker, interval, period)

        self.context['plot']       = self.__plot_context(raw_data)
        self.context['ticker']     = ticker
        self.context['stock_data'] = table_data
        self.context['form'] = TimeForm(request.GET)
    
    def __plot_context(self, data: pd.DataFrame):
        plot_data  = data.reset_index()

        sc   = StockChart(plot_data)
        plot = sc.plot()

        return plot

    # def __form_context(self, request):
    #     form = TimeForm(request.GET)
    #     if form.is_valid():
    #         interval = form.cleaned_data['interval']
    #         period   = form.cleaned_data['period']
    #     else:
    #         interval = "1m"
    #         period   = "5d"
    ############################### GET CONTEXT ##################################
         
    
    ############################### GET HELPERS ##################################
    def __handle_stock_data(self, ticker: str, interval: str, period: str) -> tuple[pd.DataFrame, list[dict]]:
        raw_data = self.sh.get_stock_data(ticker, interval, period)

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
    ############################### GET HELPERS ##################################