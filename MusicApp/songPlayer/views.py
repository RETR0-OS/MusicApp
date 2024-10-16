from lib2to3.fixes.fix_input import context

from django.http import HttpResponse, JsonResponse
from songsManager.models import Song
from itertools import chain

from django.shortcuts import render, redirect
from .models import UserPlaylist
from accounts.models import UserProfile


# Create your views here.

def dashboard(request):
    playlists = list(UserPlaylist.objects.filter(user=request.user).values())
    data = {
        "playlists": playlists,
    }
    return render(request, "showPlaylists.html", context=data)

def showPlaylist(request, pk):
    playlist = UserPlaylist.objects.get(id=pk, user=request.user)
    songs = playlist.songs.all()
    data = {
        "playlist": playlist,
        "songs": songs
    }
    return render(request, "showSongsPlaylist.html", context=data)

def loadLibrary(request):
    library = UserPlaylist.objects.filter(user=request.user)
    data = {
        "playlists": library
    }
    return render(request, "library.html", context=data)

def showFavourites(request):
    favourites = UserProfile.objects.get(user=request.user).favourite_songs.all()
    data = {
        "songs": favourites
    }
    return render(request, "showFavourites.html", context=data)

def filterPlaylistSongs(request, pk):
    try:
        query = request.GET.get("search_playlist")
        playlist = UserPlaylist.objects.get(id=pk, user=request.user)
        if query:
            songs = frozenset(chain(playlist.songs.filter(title__icontains=query),
                               playlist.songs.filter(artists__icontains=query)))
            songs_set = []
            for song in songs:
                songs_set.append(
                    {
                        "id": song.id,
                        "title":song.title,
                        "artists": song.artists,
                        "song_mp3":song.song_mp3.url
                    }
                )

            return JsonResponse({
                'status': 200,
                'data': songs_set
            })
        else:
            return JsonResponse({}, status=204)  # No content when no query
    except UserPlaylist.DoesNotExist:
        return JsonResponse({'error': 'No such playlist'}, status=404)

def filterFavouriteSongs(request):
    try:
        query = request.GET.get("search_playlist")
        print(query)
        profile = UserProfile.objects.get(user=request.user)
        if query:
            songs = frozenset(chain(profile.favourite_songs.filter(title__icontains=query),
                               profile.favourite_songs.filter(artists__icontains=query)))
            songs_set = []
            for song in songs:
                songs_set.append(
                    {
                        "id": song.id,
                        "title":song.title,
                        "artists": song.artists,
                        "song_mp3":song.song_mp3.url
                    }
                )

            return JsonResponse({
                'status': 200,
                'data': songs_set
            })
        else:
            return JsonResponse({}, status=204)  # No content when no query
    except UserPlaylist.DoesNotExist:
        return JsonResponse({'error': 'No such playlist'}, status=404)

def searchSongs(request):
    try:
        query = request.GET.get("song")
        if query:
            songs = list(frozenset(chain(Song.objects.filter(title__icontains=query), Song.objects.filter(artists__icontains=query))))[:20]
            result = []
            for song in songs:
                result.append(
                    {
                        "title":song.title,
                        "id": song.id,
                        "artists": song.artists,
                    }
                )

            data = {
                "status": 200,
                "data": result
            }

            return JsonResponse(data, status=200)
        else:
            return JsonResponse({}, status=204)

    except Song.DoesNotExist:
        return JsonResponse({'error': 'No such songs or artists'}, status=404)

def addSongToPlaylist(request, song_id, playlist_id):
    try:
        playlist = UserPlaylist.objects.get(pk=playlist_id, user=request.user)
        song = Song.objects.get(pk=song_id)
        playlist.songs.add(song)
        playlist.save()
        return JsonResponse({"data":"song added"}, status=200)
    except UserPlaylist.DoesNotExist:
        return JsonResponse({'error': 'No such playlist'}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'error': 'No such song'}, status=404)

def refresh_playlist_songs(request, playlist_id):
    playlist = UserPlaylist.objects.get(id=playlist_id, user=request.user)
    songs = playlist.songs.all()
    return render(request, 'partials/playlist_songs.html', {'songs': songs})

def refresh_favourite_songs(request):
    songs = UserProfile.objects.get(user=request.user).favourite_songs.all()
    return render(request, 'partials/playlist_songs.html', {'songs': songs})

def addSongToFavourites(request, song_id):
    song = Song.objects.get(id=song_id)
    playlist = UserProfile.objects.get(user=request.user)
    playlist.favourite_songs.add(song)
    playlist.save()
    return JsonResponse({"data": "song added to favourites"}, status=200)

def addPlaylist(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        playlist = UserPlaylist.objects.create(user=request.user, title=title, description=description, is_public=False)
        playlist.save()
        if request.FILES:
            playlist_pic = request.FILES["playlist_pic"]
            playlist.playlist_pic = playlist_pic
        playlist.save()
        return redirect("songPlayer:loadLibrary")
