from django.urls import path
from .views.all_stocks import StocksView
from .views.stock_data import StockDataView
from .views.delete_user_stock import delete_user_stock

urlpatterns = [
    path('', StocksView.as_view(), name='home'),
    path('<str:ticker>/', StockDataView.as_view(), name='stock'),
    path('user_stock/<int:user_stock_id>/delete/', delete_user_stock, name='delete_user_stock'),
]