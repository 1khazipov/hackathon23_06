from django.shortcuts import render
import re


def extract_video_id(url):
    regex = r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|https?:\/\/(?:www\.)?youtu\.be\/)([a-zA-Z0-9_-]{11})"

    match = re.search(regex, url)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


def get_data(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        text = request.POST.get('link')
        video_id = extract_video_id(text)
        return render(request, 'index.html', {'id': video_id})
    else:
        return render(request, 'index.html')
