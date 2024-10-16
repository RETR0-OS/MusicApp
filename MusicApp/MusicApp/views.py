from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        return redirect("songPlayer:songsDashboard")
    return render(request, "landing.html")