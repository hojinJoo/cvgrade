from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join

from base.base_grader import BaseGrader


class Image:
    def __init__(self, imgs):
        self.imgs = imgs
        for k in self.imgs.keys():
            if 'clean' in


class Grader_task1(BaseGrader):
    def __init__(self):
        super().__init__()
        self.prepare()
        self.img_wrapper = Image(self.imgs)
        self.task_list = ['task_1_1', 'task_1_2', 'task_2']
        self.OUTPUT = './project1/result.json'

    def grade(self, task_num, *args):
        if task_num == "task1_1":
            return self.task1_1()
        elif task_num == "task1_2":
            return self.task1_2()
        elif task_num == "task2":
            return self.task2()
        else:
            raise Exception("Wrong task num")

    def task1_1(self):
        pass

    def task1_2(self):
        pass

    def task2(self):
        pass

    def print_(self):
        print(self.imgs)


if __name__ == "__main__":
    a = Grader_task1()
    a.write_format()
