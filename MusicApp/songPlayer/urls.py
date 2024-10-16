from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = "songPlayer"

urlpatterns = [
    path('dashboard/', views.dashboard, name="songsDashboard"),
    path('playlist/<int:pk>', views.showPlaylist, name="showPlaylist"),
    path('playlist/<int:pk>/search', views.filterPlaylistSongs, name="searchPlaylistSongs"),
    path('playlist/<int:playlist_id>/add/<int:song_id>', views.addSongToPlaylist, name="addSongToPlaylist"),
    path('playlist/<int:playlist_id>/refresh_songs/', views.refresh_playlist_songs, name='refresh_playlist_songs'),
    path('dashboard/favourites/add/<int:song_id>', views.addSongToFavourites, name="addSongToFavourites"),
    path('dashboard/favourites/', views.showFavourites, name="showFavourites"),
    path('dashboard/favourites/search', views.filterFavouriteSongs, name="searchFavourites"),
    path('dashboard/favourites/refresh_songs/', views.refresh_favourite_songs, name='refresh_favourite_songs'),
    path('dashboard/library/', views.loadLibrary, name="loadLibrary"),
    path('dashboard/library/add', views.addPlaylist, name="addPlaylist")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)