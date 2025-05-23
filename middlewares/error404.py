from django.urls import resolve, Resolver404
from django.http import HttpResponseRedirect

class Error404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolve(request.path)

        except Resolver404:
            return HttpResponseRedirect(redirect_to='/error/error404/')
        
        return self.get_response(request)