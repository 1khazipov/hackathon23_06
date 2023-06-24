from django.shortcuts import render, redirect
from .utils import *

async def download_side_effect(request):
    if request.method == 'GET' and request.GET.get("link"):
        link = request.GET.get("link")
        video_id = extract_video_id(link)

        if not video_id:
            return render(request, 'index.html', {'error': 'Не валидная ссылка'})
        try:
            #todo: контент рут вынести в settings
            info = await download_youtube_video_async(link, video_id, './Downloads')
            cached = await MLPipeLineService().register_computation_task_async(link)
            if cached:
                return redirect("fdg")
            context = {"details": info}

        except:  #ResourceUnavailableException:
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
