from django.urls import path
from .views.login import LoginView
from .views.logout import log_out

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
]