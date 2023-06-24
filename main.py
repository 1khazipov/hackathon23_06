from timecodes import get_timestamped
from screenshot import ScreenshotSaver

generator = get_timestamped('/home/dima/Downloads/ru.wav')


n = ScreenshotSaver("/home/dima/Downloads/example.mp4", "/home/dima/Desktop/vscode_projects/hackaton/data_example", '/home/dima/Desktop/vscode_projects/hackaton/screenshots')
n.get_frames()
errors = n.calculate_similarity('/home/dima/Desktop/vscode_projects/hackaton/data_example')
n.save_screenshots(error_list=errors)
