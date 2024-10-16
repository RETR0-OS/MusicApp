import re
from django.shortcuts import redirect


from django.conf import settings

def mandateStaffUser(get_response):

    STAFF_URLS = getattr(settings, "STAFF_URLS", [])
    staff_urls = []
    if hasattr(settings, "STAFF_URLS"):
        staff_urls += [re.compile(url) for url in STAFF_URLS]

    def middleware(request):
        if not request.user.is_authenticated or not request.user.is_staff:
            requested_path = request.path_info
            if any(url.match(requested_path) for url in staff_urls):
                return redirect("musicApp:homePage")

        response = get_response(request)
        return response

    return middleware