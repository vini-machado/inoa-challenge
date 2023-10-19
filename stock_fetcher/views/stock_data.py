from typing import Any
from django.shortcuts import render
from django.views import View
from django import forms
from django.contrib import messages
from django.shortcuts import redirect

import pandas as pd

from ..utils.stock_handler import StockHandler
from ..utils.stock_chart import StockChart
from stock_fetcher import INTERVALS, PERIODS
from monitoring.models import UserStock

class TimeForm(forms.Form):
    interval = forms.ChoiceField(choices = INTERVALS,
                                       widget=forms.Select(attrs={'class': 'form-select'}),
                                       label="Graph Time Interval")

    period   = forms.ChoiceField(choices = PERIODS,
                                    widget=forms.Select(attrs={'class': 'form-select'}),
                                    label="Graph Time Period")
    
class TunnelPriceForm(forms.Form):
    max_price     = forms.DecimalField(label="Tunnel Maximum Price",
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}),)
    min_price     = forms.DecimalField(label="Tunnel Minimum Price",
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}),)

    periodicity   = forms.ChoiceField(choices = INTERVALS,
                                widget=forms.Select(attrs={'class': 'form-select'}),
                                label="Price Check Periodicity")


class StockDataView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = 'stock_data.html'
        self.sh            = StockHandler()
        self.context       = dict()
        self.ticker        = None
        self.interval      = '5m'
        self.period        = '5d'
        self.user_stock    = None


    def get(self, request, ticker: str):
        self.ticker   = ticker
        self.interval = request.GET.get('interval')
        self.period   = request.GET.get('period')
        
        self.__define_context(request)

        return render(request, self.template_name, self.context)
        
    ############################### GET CONTEXT ##################################
    def __define_context(self, request):
        raw_data, table_data         = self.__handle_stock_data()
        tunnel_prices, self.interval = self.__price_tunnel_context(request)

        self.context['plot']             = self.__plot_context(raw_data)
        self.context['ticker']           = self.ticker
        self.context['stock_data']       = table_data

        self.context['price_tunnel']     = TunnelPriceForm(initial = tunnel_prices)
        self.context['graph_properties'] = TimeForm(request.GET)
    
    def __plot_context(self, data: pd.DataFrame):
        plot_data  = data.reset_index()

        sc   = StockChart(plot_data)
        plot = sc.plot()

        return plot
    
    def __price_tunnel_context(self, request):
        user_stock = UserStock.objects.filter(user=request.user, stock__ticker = self.ticker)
        
        if user_stock.exists():
            self.user_stock = user_stock.first()
            max_price       = float(self.user_stock.max_price)
            min_price       = float(self.user_stock.min_price)
            periodicity     = self.user_stock.periodicity

            return { 'max_price': max_price, 'min_price': min_price, 'periodicity': periodicity }, periodicity

        return  { 'max_price': 0, 'min_price': 0, 'periodicity': self.interval }, self.interval
    
    ############################### GET CONTEXT ##################################


    ############################### GET HELPERS ##################################
    def __handle_stock_data(self) -> tuple[pd.DataFrame, list[dict]]:
        raw_data = self.sh.get_stock_data(self.ticker, self.interval, self.period)

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

    ############################### POST ##################################
    def post(self, request, ticker):
        tunnel_price = TunnelPriceForm(request.POST)
        
        self.user_stock = UserStock.objects.filter(user = request.user, stock__ticker = ticker).first()

        if tunnel_price.is_valid():

            self.user_stock.max_price   = request.POST.get('max_price')
            self.user_stock.min_price   = request.POST.get('min_price')
            self.user_stock.periodicity = request.POST.get('periodicity')

            self.user_stock.save()
            messages.success(request = request, message = "Success Registration")

        return redirect(request.get_full_path())
    ############################### POST  ##################################