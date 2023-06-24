from django.shortcuts import render, redirect
import re, os
from .utils import *

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
            #info = await download_yotube_video_async(link, './Downloads')
            cached = await MLPipeLineService().register_computation_task_async(link)
            if cached:
                return redirect("fdg")
            #context = {"details": info}
            context = {"details": {"id":"dfdfd", "title":"fdgdfgd"}}
        except ResourceUnavailableException:
            context = {"error": "video is unavailable"}

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

async def get_operation_status(request, id):
    '''
    todo: смотреть статус операции и возвращать
    {status: "pending", come_again: 30sec}
    {status: "completed", view_at: "link"}
    {status: "unregistered"}
    '''


def string_to_array(string):
    array = string.split("\n")
    return array


subtitle = 'a1\na2\na3\na4'
timecodes = '[00:00-01:01]\n[01:01-02:21]\n[02:21-03:01]\n[03:01-03:11]'
texts = 't1\nt2\nt3\nt4'
paths = 'p1\np2\np3\np4'
frames = os.listdir("static/frames")


def get_data(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        text = request.POST.get('link')
        video_id = extract_video_id(text)
        zipped_data = zip(
            string_to_array(subtitle),
            string_to_array(timecodes),
            string_to_array(texts),
            frames)
        return render(request, 'index.html', {'id': video_id, 'zipped_data': zipped_data})
    else:
        return render(request, 'index.html')
