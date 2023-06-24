from timecodes import get_timestamped, get_sentences
from screenshot import ScreenshotSaver


word_list = get_timestamped('/home/dima/Downloads/small.mp4')
sentences = get_sentences(word_list)

saver = ScreenshotSaver(
    video_path="/home/dima/Downloads/small.mp4",
    output_path="new_data_example",
    screenshots_path='new_screenshots'
)

out = saver.run_algorithm(sentences=sentences)
print(out)
