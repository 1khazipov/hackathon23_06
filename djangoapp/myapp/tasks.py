import json
import shutil
import time
import os
from django.core.cache import cache
from .main import ml_entry

from celery import shared_task

def prepareToSave(out, titles, frames):
    print("parsing")
    texts = []
    times = []
    frames = []

    for item in out:
        texts.append(item['text'])

        start_seconds = int(item['start'])
        start_time = '{:02d}:{:02d}:{:02d}'.format(start_seconds // 3600, (start_seconds % 3600) // 60,
                                                   start_seconds % 60)

        end_seconds = int(item['end'])
        end_time = '{:02d}:{:02d}:{:02d}'.format(end_seconds // 3600, (end_seconds % 3600) // 60, end_seconds % 60)

        times.append(f'[{start_time}-{end_time}]')

        frame_path = item['frame_path'].replace('\\', '/')
        frames.append(frame_path)
    frames.pop(0)

    arr = []
    for pair in titles:
        decoded_pair = ' /  '.join(pair)
        arr.append(decoded_pair)
    return arr, times, texts, frames

def save_computed(id, out, titles, frames):
    titles, times, texts, frames = prepareToSave(out, titles, frames)
    print("calculated")
    summary = {"titles": titles, 'texts': texts, 'frames': frames, 'timecodes': times}

    FILE_PATH = f'./folder/{id}.json'
    print(FILE_PATH)
    cache.set(id, summary, 60*60)
    print("cached")
    sum = cache.get(id)
    print(sum)
    #todo:
    #with open(FILE_PATH, 'w+') as outfile:
    #    json.dump(summary, outfile)
    cache.set(id, summary)


#@shared_task
def ml_pipeline(source, id, kwargs):
    try:
        text, titles, frames, options = ml_entry(source, id)
        save_computed(id, text, titles, frames)
        cache.set(f'{id}_status', {'status': 'ready'})

    except Exception as err:
        print("ошибка в пайпе")
        if options:
            shutil.rmtree(options["temp"])
        raise Exception