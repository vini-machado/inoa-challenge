from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOGIN_PAGE_NAME = 'login'
        if not request.user.is_authenticated and not request.path.startswith(reverse(LOGIN_PAGE_NAME)):
            return redirect(LOGIN_PAGE_NAME)
        response = self.get_response(request)
        return response