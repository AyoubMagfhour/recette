from django.conf import settings
from django.shortcuts import redirect

class DashboardAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/index/':
            access_count = request.session.get('dashboard_access_count', 0)
            request.session['dashboard_access_count'] = access_count + 1
        response = self.get_response(request)
        return response
