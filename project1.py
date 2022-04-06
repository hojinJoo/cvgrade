from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join

from base import BaseGrader


class Grader_task1(BaseGrader):
    def __init__(self):
        super().__init__()
        self.prepare()

    def grade(self):
        print(self.PATH)

    def print_(self):
        print(self.imgs)


# def grade():
#     imgs = {os.path.basename(img): read_image(img) if 'task1_2' in img else read_image(
#         img, False) for img in glob(join(IMG_PATH, '*'))}

#     dirs = [submission for submission in os.listdir(
#         PATH) if os.path.isdir(join(PATH, submission))]

#     for sub in dirs:
#         try:
#             student_path = join(PATH, sub)
#             zip_file = os.listdir(student_path)[0]
#             student_ID = os.path.basename(zip_file).split("_")[0]

#             with zipfile.ZipFile(join(student_path, zip_file), 'r') as zip_ref:
#                 zip_ref.extractall(student_path)

#             tasks = sorted([task for task in os.listdir(
#                 student_path) if os.path.isdir(join(student_path, task))])

#             for task in tasks:
#                 task_path = join(student_path, task)
#                 if task == "task1":
#                     for sub_task in ['denoise.py', 'noise.py']:

#                 else:

#         except Exception as e:
#             print("ERROR student ID : {}, {}".format(student_ID, e))

if __name__ == "__main__":
    a = Grader_task1()
    a.grade()
