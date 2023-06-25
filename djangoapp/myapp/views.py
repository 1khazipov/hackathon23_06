from django.shortcuts import render,Http404, redirect, HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from django.http import JsonResponse
from .utils import *
import re
import threading

def get_seconds(string):
    ints = list(map(int, string.split(':')))
    return ints[0]*60*60+ints[1]*60+ ints[2]


def get_args(params):
    kwargs = {}
    reg = re.compile(r'\d{1,2}:\d{2}:\d{2}')
    if params.get("start") and reg.match(params.get("start")):
        kwargs["start"] = get_seconds(params.get("start"))
    if params.get("stop") and reg.match(params.get("stop")):
        stop = get_seconds(params.get("stop"))
        if not kwargs.get("start") or kwargs["start"] < stop:
            kwargs['stop'] = stop
    if params.get("max") and isinstance(params.get("max"), int):
        max = int(params.get("max"))
        if max > 0:
            kwargs['max'] = max

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
            kwargs = get_args(request.POST)
            print(kwargs)
            # todo: контент рут вынести в settings, запускать скачивание внутри pipelineservice
            print(link, video_id)
            #run(link, video_id, kwargs)
            threading.Thread(target=run, args=(link, video_id, kwargs)).start()
            context = {'id': video_id, 'link': link}

        except ResourceUnavailableException:
            context = {"error": "Видео не доступно."}

        return render(request, 'loading.html', {'video_id': video_id})
    else:
        return render(request, 'index.html')


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


def get_data(request, id):
    if request.method == 'GET':
        summary = cache.get(id)
        print(summary)
        if not summary:
            return Http404()

        zipped_data = zip(
            summary['titles'],
            summary['timecodes'],
            summary['texts'],
            summary['frames'])
        return render(request, 'index.html', {'id': id, 'zipped_data': zipped_data})
    else:
        return redirect('get_data')