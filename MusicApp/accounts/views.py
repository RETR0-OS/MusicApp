from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
import uuid, base64
from django.contrib.auth import logout, login, user_logged_in, user_logged_out, user_login_failed, authenticate
from .models import UserProfile
from django.conf import settings
import requests

# Create your views here.

def generate_uuid():
    unique_id = uuid.uuid4()
    uuid_bytes = unique_id.bytes
    base64_encoded = base64.urlsafe_b64encode(uuid_bytes)
    url_friendly_uuid = base64_encoded.decode('utf-8').rstrip('=')
    return url_friendly_uuid

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        if username is not None and len(username) != 0:
            user = authenticate(request, username=username, password=password)
        else:
            return HttpResponse("<h1>Login failed!</h1>") # Fix me
        if user is not None:
            login(request, user)
            return redirect("songPlayer:songsDashboard")
        else:
            return HttpResponse("<h1>Login failed!</h1>") # Fix me

    else:
        if request.user.is_authenticated:
            return redirect("songPlayer:songsDashboard")
        else:
            return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username").lower().strip()
        password = request.POST.get("password").strip()
        first_name = request.POST.get("first_name").lower().strip()
        last_name = request.POST.get("last_name").lower().strip()
        email = request.POST.get("email").lower().strip()
        profile_pic = request.FILES.get("profile_picture")
        genres = request.POST.get("genres").lower().strip()
        user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        user_profile = UserProfile(user=user, profile_pic=profile_pic, preference_tags=genres)
        user_profile.save()
        return redirect("homePage")
    else:
        if not request.user.is_authenticated:
            return render(request, "register.html")
        else:
            return redirect("homePage")

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("homePage")

def google_login(request):
    google_auth_url = 'https://accounts.google.com/o/oauth2/auth'
    redirect_uri = 'http://localhost:8000/accounts/oauth/google/login/callback/'
    scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'

    return redirect(
        f"{google_auth_url}?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}&access_type=offline&prompt=consent"
    )

def google_callback(request):

    code = request.GET.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://oauth2.googleapis.com/token'
    redirect_uri = 'http://localhost:8000/accounts/oauth/google/login/callback/'
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }

    # Make the request to get the access token
    token_response = requests.post(token_url, data=data)
    token_info = token_response.json()
    access_token = token_info.get('access_token')

    # Retrieve user info from Google
    user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    # Now, check if the user exists, and if not, create them
    email = user_info.get('email')
    user, created = User.objects.get_or_create(email=email)

    if created:
        # Set any additional information for new users, such as name, profile pic, etc.
        user.first_name = user_info.get('given_name')
        user.last_name = user_info.get('family_name')
        user.save()
        profile = UserProfile(user=user)
        profile.profile_pic_external = user_info.get('picture')
        profile.save()
        login(request, user)
        return redirect("accounts:setProfile")
    login(request, user)
    return redirect('songPlayer:songsDashboard')

def set_profile(request):
    if request.method == "GET":
        return render(request, "selectGenres.html")
    elif request.method == "POST":
        genres = " ".join(request.POST.getlist("genres")) + request.POST.get("other_genre")
        profile = UserProfile.objects.get(user=request.user)
        profile.preference_tags = genres
        profile.save()
        return redirect('songPlayer:songsDashboard')

def load_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    data = {
        "user":profile
    }

    return render(request, "profile.html", context=data)


def edit_profile(request):
    if request.method == "GET":
        profile = UserProfile.objects.get(user=request.user)
        data = {
            "profile": profile
        }
        return render(request, "edit_profile.html", context=data)

    elif request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()

        if len(username) != 0 and len(email) != 0 and len(first_name) != 0 and len(last_name) != 0:

            profile = UserProfile.objects.get(user=request.user)
            profile.user.username = username
            profile.user.email = email
            profile.user.first_name = first_name
            profile.user.last_name = last_name

            if request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]

            profile.user.save()
            profile.save()
            return redirect("accounts:load_profile")