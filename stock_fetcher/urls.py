from django.urls import path
from .views import StocksView, StockDataView

urlpatterns = [
    path('', StocksView.as_view(), name='all_stocks'),
    path('<str:ticker>/<str:interval>', StockDataView.as_view(), name='stock'),
]