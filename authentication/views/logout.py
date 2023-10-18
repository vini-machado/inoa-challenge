from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from . import LOGIN_HTML, LOGIN_URL


def log_out(request):
    LOGOUT_MESSAGE = "Successful Logout!"
    logout(request)
    messages.success(request=request, message=LOGOUT_MESSAGE)

    return redirect(LOGIN_URL)