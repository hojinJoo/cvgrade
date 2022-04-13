from glob import glob
import os
import cv2
import zipfile
from cv2 import split
import numpy as np
import json
from os.path import join as join
import sys
import importlib
from base.base_grader import BaseGrader


class Image:
    def __init__(self, path):
        self.path = path
        self.task1_1 = cv2.imread(
            join(path, 'task1_1.jpg'), cv2.IMREAD_GRAYSCALE)
        self.task1_2 = {}
        self.task2 = {}

        self._task1_2_image()

    def get_image(self, task_num):
        return {'image': self._get_image(task_num), 'answer': self._get_answers(task_num)}

    def task2_image(self):
        pass

    def _task1_2_image(self):
        for i in range(1, 7):
            self.task1_2["task1_2_" + str(i)] = {}
            d = self.task1_2["task1_2_" + str(i)]
            d['clean'] = join(self.path, 'task1_2_'+str(i) + 'clean.jpg')
            d['noise'] = join(self.path, 'task1_2_'+str(i) + 'noise.jpg')

    def _get_image(self, task_num):
        if task_num == "1_1":
            return self.task1_1
        elif task_num == '1_2':
            return self.task1_2
        else:
            return self.task2

    def _get_answers(self, task_num):
        if task_num == "1_1":
            return {"gaussian": [29.81, 30.01], "uniform": [16.80, 16.89], "impulse": [51.74, 52.06]}
        elif task_num == "1_2":
            with open('./project1/answer.json') as r:
                answer = json.load(r)
            return a


class Grader_task1(BaseGrader):
    def __init__(self, mode):
        super().__init__(mode)

        self.OUTPUT = "./project1/result.json"
        self.SUBMISSION = "/mnt/c/Users/hj/Desktop/downloads/CV_project1"
        self.IMG_PATH = "./project1/test_images"
        self.ANSWER_PATH = "./project1/answer.json"
        self.student_ID_List_PATH = "./base/student_ID_list.json"
        self.imgs = Image(self.IMG_PATH)
        self.task_list = ['task1', 'task2']
        self._prepare()
        self._set_grades()

    def get_grade(self, task_num, path, studentID, *args):

        if task_num == "task1":
            return self.task1(path, studentID)
        elif task_num == "task2":
            return self.task2(path, studentID)
        else:
            raise Exception("Wrong task num")

    def task1(self, path, studentID):

        d = {}
        d['task1_1'] = self.task1_1(path, studentID)
        d['task1_2'] = self.task1_2(path, studentID)
        return d

    def task1_1(self, path, studentID):
        print("\n====>Grading {} task1_1\n".format(studentID))

        sys.path.append(path)
        noise = importlib.import_module('noise', ".".join(path.split("/")))

        add_gaussian_noise = getattr(noise, "add_gaussian_noise")
        add_uniform_noise = getattr(noise, 'add_uniform_noise')
        apply_impulse_noise = getattr(noise, "apply_impulse_noise")

        img_data = self.imgs.get_image('task1_1')
        img = img_data['image']
        answers = img_data['answer']

        d = {}
        gauss = add_gaussian_noise(img)
        uniform = add_uniform_noise(img)
        impulse = apply_impulse_noise(img)

        d['gaussian'] = {}
        d['gaussian']['rms'] = rms(img, gauss)

        d['uniform'] = {}
        d['uniform']['rms'] = rms(img, uniform)

        d['impulse'] = {}
        d['impulse']['rms'] = rms(img, impulse)

        for f in ['gaussian', 'uniform', 'impulse']:
            rms = d[f]['rms']
            inboundary = False
            if rms > answers[f][0] and rms < answers[f][1]:
                inboundary = True
            d[f]['in_boundary'] = inboundary

        sys.path.pop()
        del sys.modules['noise']
        return d

    def task1_2(self, path, studentID):

        print("\n====>Grading {} task1_2\n".format(studentID))
        sys.path.append(path)
        denoise = importlib.import_module(
            'denoise', '.'.join(path, split('/')))

        task1_2 = getattr(denoise, 'task1_2')
        median = getattr(denoise, 'apply_median_filter')
        bilateral = getattr(denoise, 'apply_bilateral_filter')
        my = getattr(denoise, "apply_my_filter")

        img_data = self.imgs.get_image('task1_2')
        imgs = img_data['image']
        answers = img_data['answer']

        filter_implementation = {}  # TODO:

        result_task12 = {}

        for i in range(1, 7):
            name = 'task1_2_' + str(i)
            noise_img = imgs['image'][name]['noise']
            clean_img = imgs['image'][name]['clean']
            dst = join(path, 'result.jpg')
            task1_2(noise_img, clean_img, dst)

            noise_img_read = cv2.imread(noise_img)
            result_read = cv2.imread(dst)

            rms = calculate_rms(noise_img_read, result_read)

            label = ""
            if rms < answers[name]['advanced']['RMS']:
                label = "advanced"
            elif rms < answers[name]['baseline']['RMS']:
                label = 'baseline'
            else:
                label = "out"

            result_task12[name] = {}
            result_task12[name]['rms'] = rms
            result_task12[name]['label'] = label

        sys.path.pop()
        del sys.modules['denoise']
        return result_task12

    def task2(self, path):
        pass

    def _update_dict(self, task_num, st_id, state, grade=-1):

        if task_num == 'task1':
            self.grades[st_id]['task1_1']['state'] = 1
            self.grades[st_id]['task1_2']['state'] = 1
            self.grades[st_id]['task1_1']['grade'] = grade[0]
            self.grades[st_id]['task1_2']['grade'] = grade[1]
        else:
            self.grades[st_id][task_num]['state'] = state
            self.grades[st_id][task_num]['grade'] = grade

    def _set_grades(self):
        if os.path.exists(self.OUTPUT):
            print("RESULT ALREADY EXISTS IN {}".format(self.OUTPUT))

        else:
            with open(self.student_ID_List_PATH, 'r') as r:
                self.student_id_list = json.load(r)
            for id in self.student_id_list:
                self.grades[id] = {}
                d = self.grades[id]
                d['ERROR'] = -1
                for t in self.task_list:
                    d[t] = {'state': -1}

            with open(self.OUTPUT, 'w') as w:
                json.dump(self.grades, w, indent=4)

        pass


def rms(img1, img2):
    # This function calculates RMS error between two grayscale images.
    # Two images should have same sizes.
    if (img1.shape[0] != img2.shape[0]) or (img1.shape[1] != img2.shape[1]):
        raise Exception("img1 and img2 should have the same sizes.")

    diff = np.abs(img1.astype(np.int32) - img2.astype(np.int32))

    return np.sqrt(np.mean(diff ** 2))


def calculate_rms(img1, img2):
    """
    Calculates RMS error between two images. Two images should have same sizes.
    """
    if (img1.shape[0] != img2.shape[0]) or \
            (img1.shape[1] != img2.shape[1]) or \
            (img1.shape[2] != img2.shape[2]):
        raise Exception("img1 and img2 should have same sizes.")

    diff = np.abs(img1 - img2)
    diff = np.abs(img1.astype(dtype=np.int) - img2.astype(dtype=np.int))
    return np.sqrt(np.mean(diff ** 2))


if __name__ == "__main__":
    a = Grader_task1()
    # print(a.imgs.keys())
    # print("ASd")
    # a.write_format()
