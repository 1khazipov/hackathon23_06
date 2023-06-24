from timecodes import get_timestamped, get_sentences
from screenshot import ScreenshotSaver
from speech_to_text import make_paragraphs

def ml_entry():
    word_list = get_timestamped('./djangoapp/Downloads/hffs.mp4')
    sentences = get_sentences(word_list)

    saver = ScreenshotSaver(video_path="./djangoapp/Downloads/hffs.mp4",
                    output_path="/id+timestamp/",
                    screenshots_path='/home/dima/Desktop/vscode_projects/hackaton/screenshots')

    out = saver.run_algorithm(sentences=sentences)
    print(out)


