from typing import Any
from django.shortcuts import render
from django.views import View
from django import forms
from ..models import Stock
from monitoring.models import UserStock

class StockFilterForm(forms.Form):
    tickers = forms.ModelMultipleChoiceField(
                queryset =  Stock.objects.all(),
                widget   = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                label    =  "Selecione os ativos de interesse"
    )

class StocksView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = 'all_stocks.html'
        self.stocks = Stock.objects.all()
        self.context = dict()


    ############################# GET ##################################
    def get(self, request):
        self.__get_context(request)

        return render(request, self.template_name, self.context)

    def __get_context(self, request):
        user_stocks__stocks, selected_tickers = self.__get_user_stocks(request)
        self.context['stocks'] = user_stocks__stocks
        self.context['form']   = StockFilterForm(initial={'tickers': selected_tickers})
    
        
    def __get_user_stocks(self, request):
        user_stocks__stocks = self.stocks.filter(userstock__user = request.user)
        if user_stocks__stocks.exists():
            return user_stocks__stocks, user_stocks__stocks

        return self.stocks, {}

    ############################# GET ##################################


    ############################# POST ##################################
    def post(self, request):
        self.__post_context(request)

        return render(request, self.template_name, self.context)

    def __post_context(self, request):
        stocks, form = self.__filter_stocks(request)

        self.context['stocks'] = stocks
        self.context['form']   = form

    def __filter_stocks(self, request) -> tuple[Stock, StockFilterForm]:
        form   = StockFilterForm(request.POST)
        stocks = self.stocks

        if form.is_valid():
            selected_stocks = form.cleaned_data['tickers']
            stocks = self.stocks.filter(id__in=selected_stocks)
            
            self.__save_user_stocks(stocks, request)
        return stocks, form
    
    def __save_user_stocks(self, stocks, request):
        for stock in stocks:
            user_stocks = UserStock(user = request.user, stock = stock)
            user_stocks.create_or_update(user = request.user, stock = stock)
    ############################# POST ##################################