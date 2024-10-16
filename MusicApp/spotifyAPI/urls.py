from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "spotifyAPI"

urlpatterns = [
    path("login/", views.spotify_login, name="spotifyLogin"),
    path("spotifyLoginCallback/", views.spotify_login_callback, name="spotifyLoginCallback"),
    path("GetSongs/", views.get_playlist_songs, name="spotifyGetSongs"),
    path("RefreshToken/", views.refresh_token, name="spotifyRefreshToken"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)