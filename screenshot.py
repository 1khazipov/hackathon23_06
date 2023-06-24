import sys
import argparse
import os
import cv2
import numpy as np
from pathlib import Path
from natsort import natsorted

class ScreenshotSaver:
    def __init__(self, video_path, output_path, screenshots_path, interval=1000):
        self.image_paths = []
        self.video_path = video_path
        self.output_path =  output_path
        self.screenshots_path = screenshots_path
    
    
    def get_frames(self, interval=1000):
        count = 0
        vidcap = cv2.VideoCapture(self.video_path)
        _, image = vidcap.read()

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*interval))    # added this line 
            success, image = vidcap.read()
            try:
                cv2.imwrite(self.output_path + "/frame%d.jpg" % count, image)     # save frame as JPEG file
                self.image_paths.append(self.output_path + "/frame%d.jpg" % count)
            except:
                Exception
            count += 1


    def error(self, h, w, img1, img2):
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        return mse
    

    def calculate_similarity(self, dir_path:str):
        images = os.listdir(dir_path)
        images = natsorted(images)
        error_list = []
        for i in range(len(images) - 1):
            img1 = cv2.imread(dir_path  + '/' + images[i])
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

            img2 = cv2.imread(dir_path + '/' + images[i+1])
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            h, w = img1.shape

            err = self.error(h, w, img1, img2)
            error_list.append(err)
        return error_list


    def save_screenshots(self, error_list, error_threshold=1, sequence_threshold=20):
        count = 0
        sequence = 0
        if not os.path.exists(self.screenshots_path):
            os.makedirs(self.screenshots_path)
        for error in error_list:
            if error < error_threshold:
                count += 1
                sequence += 1
            if sequence > sequence_threshold:
                sequence = 0
                img = cv2.imread(self.image_paths[count])
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(self.screenshots_path + "/frame%d.jpg" % count, img)

