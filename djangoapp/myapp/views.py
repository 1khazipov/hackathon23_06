from django.shortcuts import render, redirect, HttpResponseRedirect
from .utils import *

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
    if request.method == 'POST' and request.GET.get("link") and request.GET.get("x")\
            and request.GET.get("y") and request.GET.get("x"):
        link = request.GET.get("link") #link
        video_id = extract_video_id(link) #id

        if not video_id:
            return render(request, 'index.html', {'error': 'Не ты ссылка'})
        try:
            kwargs = get_model_params(request.GET)
            #todo: контент рут вынести в settings, запускать скачивание внутри pipelineservice
            info = await download_youtube_video_async(link, video_id, './Downloads')
            cached = await MLPipeLineService().register_computation_task_async(link, video_id, **kwargs)

            context = {"details": info, 'id': video_id}

        except ResourceUnavailableException:
            context = {"error": "Видео не доступно."}

        return render(request, 'loading.html', context)
    else:
        context = {"error": "Видео не доступно."}
        return render(request, 'index.html', {'error': "Видео не доступно."})

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


subtitle = 'Text\nText\nText\nText'
timecodes = '[00:00-01:01]\n[01:01-02:21]\n[02:21-03:01]\n[03:01-03:11]'
texts = 'Идейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.\nИдейные соображения высшего порядка, а также внедрение современных методик не даёт нам иного выбора, кроме определения модели развития. Предварительные выводы неутешительны: убеждённость некоторых оппонентов говорит о возможностях поэтапного и последовательного развития общества.'
paths = 'p1\np2\np3\np4'
frames = os.listdir("static/frames")


def get_data(request):
    if request.method == 'GET':
        text = "https://www.youtube.com/watch?v=GYB2qBwNKnc"#request.GET.get('link')
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        video_id = extract_video_id(text)
        zipped_data = zip(
            string_to_array(subtitle),
            string_to_array(timecodes),
            string_to_array(texts),
            frames)
        return render(request, 'index.html', {'id': video_id, 'zipped_data': zipped_data})
    else:
        return render(request, 'index.html')
