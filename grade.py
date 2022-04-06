from distutils.command.upload import upload
from glob import glob
from msilib.schema import Class
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join

PROJCET_NUM = "1"


class GraderParent:
    pass

class Uploader :
    pass

# 그리고 각 task 마다 GraderParent 

class Solver : 
    def __init__(self,grader,uploader):
        self.grader = grader
        self.uploader = uploader
        

def write(d, json=True):
    pass





if __name__ == "__main__":
    # grade()
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
