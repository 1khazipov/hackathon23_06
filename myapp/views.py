from django.shortcuts import render
import re, os
from .utils import *
import yt_dlp


async def download_youtube_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def extract_video_id(url):
    regex = r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|https?:\/\/(?:www\.)?youtu\.be\/)([a-zA-Z0-9_-]{11})"

    match = re.search(regex, url)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


def is_valid(url):
    return True


async def download_side_effect(request):
    if request.method == 'GET' and request.GET.get("link"):
        link = request.GET.get("link")
        print(link)
        if not is_valid(link):
            return render(request, 'index.html', {'error': 'Не валидная ссылка'})
        try:
            info = await download_yotube_video_async(link, './Downloads')
            context = {"details": info}
        except ResourceUnavailableException:
            context = {"error": "video is unavailable"}

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def string_to_array(string):
    array = string.split("\n")
    return array


subtitle = 'a1\na2\na3\na4'
timecodes = '[00:00-01:01]\n[01:01-02:21]\n[02:21-03:01]\n[03:01-03:11]'
texts = 't1\nt2\nt3\nt4'
paths = 'p1\np2\np3\np4'
frames = os.listdir("static/frames")


async def get_data(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        text = request.POST.get('link')
        await download_youtube_video(text)
        video_id = extract_video_id(text)
        zipped_data = zip(
            string_to_array(subtitle),
            string_to_array(timecodes),
            string_to_array(texts),
            frames)
        return render(request, 'index.html', {'id': video_id, 'zipped_data': zipped_data})
    else:
        return render(request, 'index.html')
