from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join

from base.base_grader import BaseGrader


class Image:
    def __init__(self, path):
        self.path = path
        self.task1_1 = original = cv2.imread(
            join(path, 'task1_1.jpg'), cv2.IMREAD_GRAYSCALE)
        self.task1_2 = {}
        for i in range(1, 7):
            self.task1_2[str(i)] = {'clean', 'noise'}
            d = self.task1_2[str(i)]
            d['clean'] = join(self.path, 'task1_2_'+str(i) + 'clean.jpg')
            d['noise'] = join(self.path, 'task1_2_'+str(i) + 'noise.jpg')
        self.task2 = {}

    def task2_image(self):
        pass

    def get_image(self, task_num):
        if task_num == "1_1":
            return self.task1_1
        elif task_num == '1_2':
            return self.task1_2
        else:
            return self.task2


class Grader_task1(BaseGrader):
    def __init__(self):
        super().__init__()
        self.prepare()
        self.imgs = Image(self.IMG_PATH)
        self.task_list = ['task1_1', 'task1_2', 'task_2']
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
    print(a.imgs.keys())
    # print("ASd")
    # a.write_format()
