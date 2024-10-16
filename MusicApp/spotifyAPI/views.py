from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime
import urllib.parse
import requests


# Create your views here.

client_id = getattr(settings, "CLIENT_ID", None)
client_secret = getattr(settings, "CLIENT_SECRET", None)
api_base_url = getattr(settings, "API_BASE_URL", None)
api_token_url = getattr(settings, "API_TOKEN_URL", None)
api_auth_url = getattr(settings, "SPOTIFY_AUTH_URL", None)
api_callback_url = getattr(settings, "SPOTIFY_CALLBACK_URI", None)

@staff_member_required
def spotify_login(request):
    '''
    This function authenticates the bot to spotify's api
    :param request: WSGI request object of Django
    :return: a redirect to the authentication website of spotify
    '''

    scope = "playlist-read-private, playlist-read-collaborative user-read-private user-read-email"

    request_body = {
        "client_id" : client_id,
        "response_type" : "code",
        "redirect_uri" : api_callback_url,
        "scope" : scope,

    }

    auth_url = api_auth_url + "?" + urllib.parse.urlencode(request_body)
    return redirect(auth_url)

@staff_member_required
def spotify_login_callback(request):

    '''
        This function catches the callback of the Spotify API and sets the access_token, expiry time and the refresh token return for the session
        :param request: WSGI request object of Django.
        :return: the access_token, refresh_token, and time of expiry
    '''

    if "error" in request.GET:
        return HttpResponse(f"<h1> Error:{request.GET.get("error")}</h1>")
    elif "code" in request.GET:
        request_body = {
            "code": request.GET.get("code"),
            "grant_type": "authorization_code",
            "redirect_uri": api_callback_url,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        token_info = requests.post(api_token_url, data=request_body).json()

        request.session["access_token"] = token_info["access_token"]
        request.session["refresh_token"] = token_info["refresh_token"]
        request.session["token_expiry"] = datetime.now().timestamp() + token_info["expires_in"]

        ret_data ={
            "access_token": token_info["access_token"],
            "refresh_token": token_info["refresh_token"],
            "token_expiry": datetime.now().timestamp() + token_info["expires_in"]
        }

        return redirect("spotifyAPI:spotifyGetSongs")
    return redirect("spotifyAPI:spotifyLogin")

@staff_member_required
def get_playlist_songs(request):

    '''
    Gets the song names from a particular playlist and returns the song names as json object.
    :param request:
    :return: json object containing number of songs, list of song names
    '''

    if "access_token" not in request.session:
        return redirect("spotifyAPI:spotifyLogin")
    elif datetime.now().timestamp() >= request.session.get("token_expiry"):
        return redirect("spotifyAPI:spotifyRefreshToken")
    headers ={
        "Authorization": f"Bearer {request.session.get('access_token')}",
    }

    playlists = requests.get(api_base_url + "me/playlists", headers=headers).json()["items"]

    playlist_id = None
    num_songs = 0
    for playlist in playlists:
        if playlist["name"] == getattr(settings, "SPOTIFY_SONGS_PLAYLIST_NAME", None):
            playlist_id = playlist["id"]
            num_songs = playlist["tracks"]["total"]
            break
    playlist_items = []
    for i in range(num_songs // 20):
        playlist_items.extend(list(requests.get(getattr(settings, "API_BASE_URL", None) + f"playlists/{playlist_id}/tracks?offset={(20*i)+1}",
                     headers=headers).json()["items"]))
    playlist_items.extend(list(requests.get(getattr(settings, "API_BASE_URL", None) + f"playlists/{playlist_id}/tracks?offset={20*(num_songs // 20)}",
                 headers=headers).json()["items"]))
    ids = []
    for song in playlist_items:
        ids.append(song.get("track").get("id"))
    ids = frozenset(ids)
    print(len(ids))
    song_names = {}
    for counter, song_id in enumerate(ids):
        request_url = getattr(settings, "API_BASE_URL", None) + f"tracks/{song_id}"
        song = requests.get(request_url, headers=headers).json()
        song_name = song.get("name")
        artists = ", ".join([x.get("name") for x in song.get("artists")])
        song_names[counter] = [song_name, artists]
    request.session["song_data"] = song_names
    return redirect("songsManager:downloadSongs")

@staff_member_required
def refresh_token(request):
    if "refresh_token" not in request.session:
        return redirect("spotifyAPI:spotifyLogin")
    elif datetime.now().timestamp() > request.session["token_expiry"]:
        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": request.session["refresh_token"],
            "client_id": getattr(settings, "CLIENT_ID", None),
            "client_secret": getattr(settings, "CLIENT_SECRET", None)
        }

        response = requests.post(getattr(settings, 'API_TOKEN_URL', None), data=request_body)

        new_token_info = response.json()

        request.session["access_token"] = new_token_info["access_token"]
        request.session["token_expiry"] = datetime.now().timestamp() + new_token_info["expires_in"]

        ret_data = {
            "access_token": new_token_info["access_token"],
            "token_expiry": datetime.now().timestamp() + new_token_info["expires_in"]
        }
        return redirect("spotifyAPI:spotifyLogin")
    else:
        return redirect("spotifyAPI:spotifyLogin")