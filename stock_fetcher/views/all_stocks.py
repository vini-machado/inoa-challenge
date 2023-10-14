from typing import Any
from django.shortcuts import render
from django.views import View
from django import forms
from ..models import Stock
from ..utils.stock_handler import StockHandler

class StockFilterForm(forms.Form):
    forms = forms.ModelMultipleChoiceField(
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
        self.__get_context()

        return render(request, self.template_name, self.context)

    def __get_context(self):
        self.context['stocks'] = self.stocks
        self.context['form']   = StockFilterForm()
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
            selected_stocks = form.cleaned_data['forms']
            stocks = self.stocks.filter(id__in=selected_stocks)

        return stocks, form
    ############################# POST ##################################