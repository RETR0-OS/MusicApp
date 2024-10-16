from django.urls import path, include
from .views import download_songs
from django.conf.urls.static import static
from django.conf import settings
from songPlayer.views import searchSongs

app_name = "songsManager"

urlpatterns = [
    path('download/', download_songs, name="downloadSongs"),
    path('search', searchSongs, name="searchSongs"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)