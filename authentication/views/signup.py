from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .register_form import RegisterForm
from django.contrib import messages
from . import SIGNUP_URL, SIGNUP_HTML

class SignupView(View):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.template_name = SIGNUP_HTML
        self.context = dict()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        if not self.context.get('form'):
            self.context['form'] = RegisterForm()

        return render(request, self.template_name, self.context)

    
    def post(self, request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(username = username, password = password)

            user.email = email
            user.save(update_fields=['email'])

            login(request, user)
            
            messages.success(request = request, message = "Success Registration")
            
            self.context['form'] = form
            return redirect('home')
        
        messages.success(request = request, message = "Contact Administration")
        return redirect(SIGNUP_URL)
