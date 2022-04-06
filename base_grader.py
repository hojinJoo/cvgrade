from abc import abstractmethod
from distutils.command.upload import upload
from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join


class BaseGrader:
    def __init__(self):
        self.SUBMISSION = "/mnt/d/chrome/COMPUTER VISION (CSI4116.01-00)-Project1-2736970"
        self.IMG_PATH = "/mnt/d/workspace/else/cvgrade/project1/test_images"
        self.ANSWER_PATH = "/mnt/d/workspace/else/cvgrade/project1/answer.json"

    def read_image(self, img, color=True):
        if color:
            return cv2.cvtColor(cv2.imread(img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        else:
            return cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    def prepare(self):
        self.imgs = {os.path.basename(img): self.read_image(img) if 'task1_2' in img else self.read_image(
            img, False) for img in glob(join(self.IMG_PATH, '*'))}
        self.dirs = [submission for submission in os.listdir(
            self.PATH) if os.path.isdir(join(self.PATH, submission))]

    @abstractmethod
    def get_grade(self, task_num):
        pass

    def grade_all(self):
        grade = {}
        for sub in self.dirs:
            try:
                student_path = join(self.SUBMISSION, sub)
                zip_file = os.listdir(student_path)[0]
                student_ID = os.path.basename(zip_file).split("_")[0]

            with zipfile.ZipFile(join(student_path, zip_file), 'r') as zip_ref:
                zip_ref.extractall(student_path)

            tasks = sorted([task for task in os.listdir(
                student_path) if os.path.isdir(join(student_path, task))])

            for task in tasks:
                task_path = join(student_path, task)
                if task == "task1":
                    for sub_task in ['denoise.py', 'noise.py']:
                        self.get_grade()
                else:

        except Exception as e:
            print("ERROR student ID : {}, {}".format(student_ID, e))

        return grade


class Solver:
    def __init__(self, grader, uploader):
        self.grader = grader
        self.uploader = uploader


def write(d, json=True):
    pass


if __name__ == "__main__":
    pass
