import datetime

from .timecodes import get_timestamped, get_sentences
from .screenshot import ScreenshotSaver
import os

def ml_entry(source, id,):
    word_list = get_timestamped(source)
    sentences = get_sentences(word_list)
    time = datetime.datetime.now()
    timestamp = f'{time.year}{time.month}{time.day}{time.second}'
    temp = os.path.join("temp",f'{id}_{timestamp}')
    frames = os.path.join("frames", f'{id}')
    saver = ScreenshotSaver(video_path=source,
                    output_path= temp,
                    screenshots_path=frames)

    out = saver.run_algorithm(sentences=sentences)
    os.remove(temp)

    return out, frames


