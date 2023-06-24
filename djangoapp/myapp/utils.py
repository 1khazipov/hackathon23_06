import yt_dlp
import pytube
import asyncio
import os.path
from django.core.cache import cache
import re
from .Exceptions.exceptions import ResourceUnavailableException
from .tasks import ml_pipeline

def run(url, id):
    download_youtube_video(url, id, './Downloads')
    key = f'{id}_status'
    registered = cache.get(key)
    if registered and registered['status'] == 'pending':
        return

    cache.set(key, {'status': 'pending'})
    ml_pipeline(url, id)


def download_youtube_video(url, video_id, destination):
    print(destination)
    destination = os.path.join(destination, f'{video_id}.mp4')

    if not os.path.exists(destination):
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': destination,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def extract_video_id(url):
    if url is not None:
        regex = r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|https?:\/\/(?:www\.)?youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        if match:
            video_id = match.group(1)
            return video_id

    return None