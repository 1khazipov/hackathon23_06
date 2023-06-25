from timecodes import get_timestamped, get_sentences
from screenshot import ScreenshotSaver
from summarizer import create_title


VIDEO_PATH = '/home/dima/Downloads/test1.mp4'
word_list = get_timestamped(VIDEO_PATH)
sentences = get_sentences(word_list)

saver = ScreenshotSaver(
    video_path=VIDEO_PATH,
    output_path="new_data_example",
    screenshots_path='new_screenshots'
)

out_dict = saver.run_algorithm(sentences=sentences)

titles = [create_title(x.get('text'), num_return_sequences=2) for x in out_dict]

print(out_dict)
