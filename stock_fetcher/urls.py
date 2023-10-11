from django.urls import path
from . import views

urlpatterns = [
    path('stock_fetcher/', views.stock_data, name='stock_fetcher'),
]