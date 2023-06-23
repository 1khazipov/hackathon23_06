from django.shortcuts import render
import re
from .utils import *
from django.views.generic import TemplateView

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

