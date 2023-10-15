from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . import LOGIN_HTML, LOGIN_URL, STOCKS_URL


class LoginView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = LOGIN_HTML
        self.context = dict()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(STOCKS_URL)
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(STOCKS_URL)
        else:
            ERROR_MESSAGE = "Login Failed"
            messages.error(request = request, message = ERROR_MESSAGE)

            return redirect(LOGIN_URL)