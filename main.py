from timecodes import get_timestamped, get_sentences
from screenshot import ScreenshotSaver
#from speech_to_text import make_paragraphs

word_list = get_timestamped('/home/dima/Downloads/small.mp4')
sentences = get_sentences(word_list)

saver = ScreenshotSaver(video_path="/home/dima/Downloads/small.mp4",
                    output_path="/home/dima/Desktop/vscode_projects/hackaton/data_example",
                    screenshots_path='/home/dima/Desktop/vscode_projects/hackaton/screenshots')

out = saver.run_algorithm(sentences=sentences)
print(out)


