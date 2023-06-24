from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from django.http import JsonResponse
from .utils import *
import json
import threading


def tryParseFloat(value):
    try:
        value = float(value)
        return value
    except ValueError:
        return None


def get_model_params(get):
    kwargs = {}
    start = None
    if get.get("start"):
        res = tryParseFloat(get.get("start"))
        if res and res >= 0:
            kwargs['start'] = res
            start = res

    if get.get("stop"):
        res = tryParseFloat(get.get("stop"))
        if res and res >= 0:
            if start != None and start < res:
                kwargs['stop'] = res

    return kwargs


async def download_side_effect(request):
    if request.method == 'POST':
        # x = request.GET.get("x")
        # y = request.GET.get("y")
        # z = int(request.GET.get("z"))
        link = request.POST.get("link")  # link
        video_id = extract_video_id(link)  # id
        print(link)
        print(video_id)
        if not video_id:
            return render(request, 'index.html', {'error': 'Не ты ссылка'})
        try:
            kwargs = {}  # get_model_params(request.GET)
            # todo: контент рут вынести в settings, запускать скачивание внутри pipelineservice
            info = {'id': video_id, 'link': link}
            print(link, video_id)
            threading.Thread(target=run, args=(link, video_id)).start()
            context = {"details": info}

        except ResourceUnavailableException:
            context = {"error": "Видео не доступно."}

        return render(request, 'loading.html', {'video_id': video_id})
    else:
        context = {"error": "Видео не доступно."}
        return render(request, 'index.html', {'error': "Видео не доступно."})


async def get_operation_status(request, id):
    key = f'{id}_status'
    cached = cache.get(key)
    if cached:
        return JsonResponse({"status": cached['status']})
    return JsonResponse({'status': 'unregistered'})
    # '''
    # todo: смотреть статус операции и возвращать
    # {status: "pending", come_again: 30sec}
    # {status: "completed", view_at: "link"}
    # {status: "unregistered"}
    # '''


def string_to_array(string):
    array = string.split("\n")
    return array


subtitle = 'Text\nText\nText\nText'
timecodes = '[00:00-01:01]\n[01:01-02:21]\n[02:21-03:01]\n[03:01-03:11]'
texts = 'Идейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.'
paths = 'p1\np2\np3\np4'
frames = os.listdir("static/frames")


def get_data(request):
    if request.method == 'GET':
        text = "https://www.youtube.com/watch?v=GYB2qBwNKnc"  # request.GET.get('link')
        video_id = extract_video_id(text)
        zipped_data = zip(
            string_to_array(subtitle),
            string_to_array(timecodes),
            string_to_array(texts),
            frames)
        return render(request, 'index.html', {'id': video_id, 'zipped_data': zipped_data})
    else:
        return render(request, 'index.html')
