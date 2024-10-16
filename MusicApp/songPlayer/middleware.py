import re
from django.shortcuts import redirect
from django.conf import settings

def requireLoginMiddleware(get_response):
    LOGIN_EXEMPT_URLS = getattr(settings, "LOGIN_EXEMPT_URLS", [])
    login_exempt_urls = [re.compile(url) for url in LOGIN_EXEMPT_URLS]

    def middleware(request):
        if not request.user.is_authenticated:
            requested_path = request.path_info
            if not any(url.match(requested_path) for url in login_exempt_urls):
                return redirect("accounts:login")
        response = get_response(request)
        return response

    return middleware
