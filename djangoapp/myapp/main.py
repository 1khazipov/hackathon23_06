import datetime

from .timecodes import get_timestamped, get_sentences
from .screenshot import ScreenshotSaver
import os, shutil
from .summarizer import create_title

def ml_entry(source, id,):
    word_list = get_timestamped(source)
    sentences = get_sentences(word_list)
    time = datetime.datetime.now()
    timestamp = f'{time.year}{time.month}{time.day}{time.second}'
    temp = os.path.join("temp",f'{id}_{timestamp}')
    frames = os.path.join("static","frames", f'{id}')
    saver = ScreenshotSaver(video_path=source,
                    output_path= temp,
                    screenshots_path=frames)

    out_dict = saver.run_algorithm(sentences=sentences)

    titles = [create_title(x.get('text'), num_return_sequences=2) for x in out_dict]
    #shutil.rmtree(temp)

    #import json
    #with open("C:\hackaton\hackathon23_06\djangoapp\my.json", "w", encoding="utf-8") as file:
    #    json.dump(out_dict, file)
    #with open("C:\hackaton\hackathon23_06\djangoapp\mtitlea.json", "w", encoding="utf-8") as file:
    #    json.dump(titles, file)
    print("finished")
    return out_dict, titles, frames, temp


