from django.urls import path
from .views.all_stocks import StocksView
from .views.stock_data import StockDataView

urlpatterns = [
    path('', StocksView.as_view(), name='all_stocks'),
    path('<str:ticker>/', StockDataView.as_view(), name='stock'),
]