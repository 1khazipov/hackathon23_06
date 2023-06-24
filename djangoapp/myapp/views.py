from django.shortcuts import render
from django.http import JsonResponse
from .utils import *

def tryParseFloat(value):
    try:
        value = float(str(value))
        return value
    except ValueError:
        return None

def tryParseInt(value):
    try:
        value = int(str(value))
        return value
    except ValueError:
        return None

def get_model_params(get):
    kwargs = {
        'start':tryParseFloat(get.get('start')),
        'stop': tryParseFloat(get.get('stop')),
        'max-symbols': tryParseInt(get.get('max-symbols'))
    }

    kwargs2 = {}
    if kwargs.get('start') and kwargs.get('start') >=0:
        kwargs2['start'] = kwargs.get('start')
    if kwargs.get('stop') and kwargs['stop'] >=0:
        if kwargs2.get('start') != None and kwargs.get('stop') >= kwargs.get('start') or kwargs.get('start') == None:
            kwargs2['stop'] = kwargs['stop']
    if kwargs.get('max-symbols') and kwargs.get('max-symbols') >=0:
        kwargs2['max-symbols'] = kwargs['max-symbols']

    return kwargs2

async def download_side_effect(request):
    if request.method == 'POST' and request.GET.get("link") and request.GET.get("x")\
            and request.GET.get("y") and request.GET.get("x"):
        link = request.GET.get("link") #link
        video_id = extract_video_id(link) #id

        if not video_id:
            return render(request, 'index.html', {'error': 'Не ты ссылка'})
        try:
            kwargs = get_model_params(request.GET)
            print(kwargs.get('max-symbols'))
            #todo: контент рут вынести в settings, запускать скачивание внутри pipelineservice
            info = await download_youtube_video_async(link, video_id, './Downloads')
            MLPipeLineService().register_computation_task_async(link, video_id, **kwargs)

            context = {"details": info }

        except ResourceUnavailableException:
            context = {"error": "Видео не доступно."}

        return render(request, 'loading.html', context)
    else:
        context = {"error": "Видео не доступно."}
        return render(request, 'index.html', {'error': "Видео не доступно."})

async def get_operation_status(request, id):
    key = f'{id}_status'
    cached = cache.get(key)
    if cached:
        return JsonResponse({"status": cached['status']})
    return JsonResponse({'status': 'unregistered'})
    '''
    todo: смотреть статус операции и возвращать
    {status: "pending", come_again: 30sec}
    {status: "completed", view_at: "link"}
    {status: "unregistered"}
    '''


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
        text = "https://www.youtube.com/watch?v=GYB2qBwNKnc"#request.GET.get('link')
        video_id = extract_video_id(text)
        zipped_data = zip(
            string_to_array(subtitle),
            string_to_array(timecodes),
            string_to_array(texts),
            frames)
        return render(request, 'index.html', {'id': video_id, 'zipped_data': zipped_data})
    else:
        return render(request, 'index.html')
