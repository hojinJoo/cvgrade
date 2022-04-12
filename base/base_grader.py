from abc import abstractmethod
from glob import glob
import os
from re import L
from turtle import st
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join

#__all__ = ["BaseGrader"]


class BaseGrader:
    def __init__(self):
        self.SUBMISSION = "/mnt/d/chrome/COMPUTER VISION (CSI4116.01-00)-Project1-2736970"
        self.IMG_PATH = "./project1/test_images"
        self.ANSWER_PATH = "/mnt/d/workspace/else/cvgrade/project1/answer.json"
        self.student_ID_List_PATH = "./base/student_ID_list.json"
        with open(self.student_ID_List_PATH, 'r') as r:
            self.student_id_list = json.load(r)
        self.task_list = []
        self.OUTPUT = ""

    def write(self):
        # TODO
        pass

    def write_format(self):
        if not os.path.exists(self.OUTPUT):
            d = {}
            for st_id in self.student_id_list:
                d[st_id] = {}
                t = d[st_id]
                for task in self.task_list:
                    t[task] = -1
            with open(self.OUTPUT, 'w') as w:
                json.dump(d, w, indent=4)
        else:
            print("Result Already Exists at {}".format(self.OUTPUT))
            pass

    def update_json(self, student_ID, task, grade):
        self.OUTPUT[student_ID][task] = grade
        with open(self.OUTPUT, 'w') as w:
            json.dump(self.OUTPUT, w)
        with open(self.OUTPUT, 'r') as r:
            self.OUTPUT = json.load(r)

    def is_done(self, student_ID, task):
        # TODO
        return self.OUTPUT[student_ID][task] != -1

    def read_image(self, img, color=True):
        if color:
            return cv2.cvtColor(cv2.imread(img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        else:
            return cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    def prepare(self):
        # self.imgs = {os.path.basename(img): self.read_image(img) if 'task1_2' in img else self.read_image(
        #     img, False) for img in glob(join(self.IMG_PATH, '*'))}
        self.dirs = [submission for submission in os.listdir(
            self.SUBMISSION) if os.path.isdir(join(self.SUBMISSION, submission))]

    @abstractmethod
    def get_grade(self, task_num, *args):
        pass

    # def grade_all(self):
    #     grade = {}
    #     for sub in self.dirs:
    #         try:
    #             student_path = join(self.SUBMISSION, sub)
    #             zip_file = os.listdir(student_path)[0]
    #             student_ID = os.path.basename(zip_file).split("_")[0]

    #         with zipfile.ZipFile(join(student_path, zip_file), 'r') as zip_ref:
    #             zip_ref.extractall(student_path)

    #         tasks = sorted([task for task in os.listdir(
    #             student_path) if os.path.isdir(join(student_path, task))])

    #         for task in tasks:
    #             task_path = join(student_path, task)
    #             if task == "task1":
    #                 for sub_task in ['denoise.py', 'noise.py']:
    #                     self.get_grade()
    #             else:
    #                 pass

    #         except Exception as e:
    #             print("ERROR student ID : {}, {}".format(student_ID, e))

    #     return grade


if __name__ == "__main__":
    pass
