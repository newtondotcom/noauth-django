# middleware.py
from django.http import JsonResponse
from db.models import *

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key_allowed_endpoints = ['']
        print("Api Key Middleware initialized") 

    def __call__(self, request):
        api_key_header = request.headers.get('Authorization')
        cleanedPath = request.path.split("/")[0]

        if request.META.get('REMOTE_ADDR') == '127.0.0.1' or request.META.get('REMOTE_ADDR') == '::1':
            response = self.get_response(request)
            return response

        if not cleanedPath.count("verif") > 0 and not cleanedPath.count("admin") > 0 and cleanedPath.count("test_users") > 0 and cleanedPath not in self.api_key_allowed_endpoints:
            if api_key_header and api_key_header.startswith('Api-Key '):
                api_key = api_key_header.split(' ')[1]
                keys = ["69f13396-66d1-4736-873e-0ddd2ba476ea","f3e3e3e3-66d1-4736-873e-0ddd2ba476ea"]
                if keys.count(api_key) == 0:
                    return JsonResponse({'error': 'Invalid API key'}, status=403)

            else:
                return JsonResponse({'error': 'API key missing or invalid'}, status=401)

        response = self.get_response(request)
        return response
