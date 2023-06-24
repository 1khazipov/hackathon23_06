from timecodes import get_timestamped, get_sentences
from screenshot import ScreenshotSaver
from summarizer import create_title


video_path = '/home/dima/Downloads/example.mp4'
word_list = get_timestamped(video_path)
sentences = get_sentences(word_list)

saver = ScreenshotSaver(
    video_path=video_path,
    output_path="new_data_example",
    screenshots_path='new_screenshots'
)

out_dict = saver.run_algorithm(sentences=sentences)

titles = [create_title(x.get('text')) for x in out_dict]

