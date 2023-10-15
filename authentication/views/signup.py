from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . import SIGNUP_URL, SIGNUP_HTML, STOCKS_URL

class SignupView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = SIGNUP_HTML
        self.context = dict()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(STOCKS_URL)

        if not self.context.get('form'):
            self.context['form'] = UserCreationForm()

        return render(request, self.template_name, self.context)

    
    def post(self, request):
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(username = username, password = password)
            login(request, user)
            
            messages.success(request = request, message = "Success Registration")
            
            self.context['form'] = form
            return redirect(STOCKS_URL)
        
        messages.success(request = request, message = "Contact Administration")
        return redirect(SIGNUP_URL)
