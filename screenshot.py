import os
import shutil
import cv2
import numpy as np
from natsort import natsorted
import math


class ScreenshotSaver:
    def __init__(
            self,
            video_path,
            output_path,
            screenshots_path,
            interval=1000,
            error_threshold=0.8,
            sequence_threshold=20
    ):
        self.image_paths = []
        self.video_path = video_path
        self.output_path = output_path
        self.screenshots_path = screenshots_path
        self.screenshots_paths = [" "]
        self.screenshots_time = []
        self.interval = interval
        self.error_threshold = error_threshold
        self.sequence_threshold = sequence_threshold

    def get_frames(self):
        count = 0
        vidcap = cv2.VideoCapture(self.video_path)
        _, image = vidcap.read()

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        else:
            shutil.rmtree(self.output_path)
            os.makedirs(self.output_path)

        success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * self.interval))
            success, image = vidcap.read()
            try:
                cv2.imwrite(self.output_path + "/frame%d.jpg" % count, image)
                self.image_paths.append(
                    self.output_path + "/frame%d.jpg" % count)
            except Exception:
                print("All images have been saved")
            count += 1

    def error(self, h, w, img1, img2):
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))

        return mse

    def calculate_similarity(self):
        images = os.listdir(self.output_path)
        images = natsorted(images)
        error_list = []
        for i in range(len(images) - 1):
            img1 = cv2.imread(self.output_path + '/' + images[i])
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            img2 = cv2.imread(self.output_path + '/' + images[i+1])
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            h, w = img1.shape

            err = self.error(h, w, img1, img2)
            error_list.append(err)
        self.error_list = error_list.copy()
        return error_list

    def save_screenshots(self):
        count = 0
        sequence = 0

        if not os.path.exists(self.screenshots_path):
            os.makedirs(self.screenshots_path)
        else:
            shutil.rmtree(self.screenshots_path)
            os.makedirs(self.screenshots_path)

        for error in self.error_list:
            if error < self.error_threshold:

                sequence += 1
            if sequence > self.sequence_threshold:
                try:
                    sequence = 0
                    img = cv2.imread(self.image_paths[count])
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(self.screenshots_path +
                                "/frame%d.jpg" % count, img)
                    self.screenshots_time.append(
                        count - self.sequence_threshold)
                    self.screenshots_paths.append(
                        self.screenshots_path + "/frame%d.jpg" % count)
                except Exception:
                    print("WTF EXCEPTION", count)
                    pass
            count += 1
        return self.screenshots_time, self.screenshots_paths

    def text_plus_screenshot(self, sentences):
        sentences_time = [x.get('start') for x in sentences]
        indexes = []
        paragraphs = []
        str1 = ""

        for screenshot_time in self.screenshots_time:
            index = lowestGreaterThan(sentences_time, screenshot_time)
            indexes.append(index)

        start_paragraph = []
        end_paragraph = []
        end = 0
        for i in range(len(sentences)):
            if sentences[i].get('start') < sentences[indexes[0]].get('start'):
                str1 += sentences[i].get('text')
                end = sentences[i].get('end')
            else:
                if i > 0:
                    start = sentences[0].get('start')
                    paragraphs.append(str1)
                    start_paragraph.append(start)
                    end_paragraph.append(end)
                    break
        str1 = ""

        k = indexes[0]
        start_paragraph.extend([sentences[x].get('start') for x in indexes.copy()])
        end_paragraph.extend([sentences[x].get('end') for x in indexes[1:].copy()])
        end_paragraph.append(sentences[-1].get('end'))

        for index in indexes[1:]:
            while sentences_time[k] < sentences_time[index]:
                str1 += sentences[k].get('text')
                k += 1
            else:
                paragraphs.append(str1)
                str1 = ""
        str1 = ""

        for i in range(indexes[-1], len(sentences)):
            str1 += sentences[i].get('text')
        paragraphs.append(str1)

        return paragraphs, start_paragraph, end_paragraph

    def run_algorithm(self, sentences):
        self.get_frames()
        self.calculate_similarity()
        self.save_screenshots()
        paragraphs, start_paragraph, end_paragraph = self.text_plus_screenshot(
            sentences=sentences
        )

        output_dict = {
            'text': "",
            'start': "",
            'end': "",
            'frame_path': ""
        }

        output_list = []
        for i in range(len(paragraphs)):
            output_dict = {
                'text': paragraphs[i],
                'start': start_paragraph[i],
                'end': end_paragraph[i],
                'frame_path': self.screenshots_paths[i]
            }
            output_list.append(output_dict)

        return output_list


def lowestGreaterThan(arr, threshold):
    low = 0
    high = len(arr)

    while low < high:
        mid = math.floor((low + high) / 2)

        if arr[mid] == threshold:
            return mid
        elif arr[mid] < threshold and mid != low:
            low = mid
        elif arr[mid] > threshold and mid != high:
            high = mid
        else:
            high = low = low + 1

    return low
