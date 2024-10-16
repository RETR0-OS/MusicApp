from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from youtubesearchpython import VideosSearch
from pytube import YouTube
import uuid
import base64
from .models import Song

def generate_uuid():
    unique_id = uuid.uuid4()
    uuid_bytes = unique_id.bytes
    base64_encoded = base64.urlsafe_b64encode(uuid_bytes)
    url_friendly_uuid = base64_encoded.decode('utf-8').rstrip('=')
    return url_friendly_uuid

def audio_downloader(search_query):
    download_path = str(getattr(settings, "MEDIA_ROOT", None)) + "/songs"
    vid_search = VideosSearch(search_query, limit=1)
    link = vid_search.result()["result"][0]["link"]
    try:
        video = YouTube(link)
        audio = video.streams.filter(only_audio=True).first()
        new_filename = generate_uuid()
        audio.download(output_path=download_path, filename=new_filename+".mp3")
        return new_filename+".mp3"
    except Exception as error:
        print(error)
        return None

def download_songs(request):
    if "song_data" in request.session:
        songs = request.session.get("song_data")
        total = len(songs)
        downloaded_songs = 0
        for song in songs:
            audio = audio_downloader(f"{songs[song][0]} by {songs[song][1]}")
            if audio is not None:
                title = songs[song][0]
                file_name = audio
                song = Song.objects.create(title=title, artists=songs[song][1])
                song.song_mp3.name = f"songs/{file_name}"
                song.save()
                downloaded_songs += 1
            else:
                continue
        return HttpResponse(f"<h1> {downloaded_songs}/{total} downloaded successfully")
    return redirect("spotifyAPI:spotifyGetSongs")