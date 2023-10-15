from django.shortcuts import redirect
from django.urls import reverse
from functools import reduce


BYPASS_PAGES = ['login', 'signup']
class AuthenticationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOGIN_PAGE_NAME = 'login'
        if not request.user.is_authenticated and not self.__bypass_auth_pages(request):
            return redirect(LOGIN_PAGE_NAME)
        response = self.get_response(request)
        return response
    
    def __bypass_auth_pages(self, request) -> bool:
        path_start = lambda path: request.path.startswith(path)
        
        pages = [reverse(path) for path in BYPASS_PAGES]
        pages.append('/admin/')

        return reduce(lambda result, path: result or path_start(path), pages, False)