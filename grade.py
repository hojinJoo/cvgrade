from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join
PATH = "/mnt/d/chrome/COMPUTER VISION (CSI4116.01-00)-Project1-2736970"
IMG_PATH = "/mnt/d/workspace/else/test_images"


def read_image(img, color=True):
    if color:
        return cv2.cvtColor(cv2.imread(img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    else:
        return cv2.imread(img, cv2.IMREAD_GRAYSCALE)


def write(d, json=True):
    pass


def grade():
    imgs = {os.path.basename(img): read_image(img) if 'task1_2' in img else read_image(
        img, False) for img in glob(join(IMG_PATH, '*'))}

    dirs = [submission for submission in os.listdir(
        PATH) if os.path.isdir(join(PATH, submission))]

    for sub in dirs:
        try:
            student_path = join(PATH, sub)
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

                else:
                    pass
        except Exception as e:
            print("ERROR student ID : {}, {}".format(student_ID, e))


if __name__ == "__main__":
    grade()
    # d = {}
    # for imgs in glob(join(IMG_PATH, '*')):
    #     if "clean" in imgs:
    #         continue
    #     name = os.path.basename(imgs).split(".")[0]
    #     name = name[:-6]
    #     d[name] = {}
    #     d[name]["advanced"] = {'Filter': None, "RMS": None}
    #     d[name]["baseline"] = {'Filter': None, "RMS": None}
    # with open('answer.json', 'w') as out:
    #     json.dump(d, out, indent=4)
