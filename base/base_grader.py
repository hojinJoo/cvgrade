from abc import abstractmethod
from glob import glob
import os
import cv2
import zipfile
import numpy as np
import json
from os.path import join as join
import shutil
import sys
#__all__ = ["BaseGrader"]


DONE = 1
ERROR = -1


class BaseGrader:
    def __init__(self, mode):
        self.SUBMISSION = ""
        self.IMG_PATH = ""
        self.ANSWER_PATH = ""
        self.student_ID_List_PATH = "."
        self.task_list = []
        self.OUTPUT = ""
        self.grades = {}
        self.mode = mode

    @abstractmethod
    def get_grade(self, task_num, path, studentID, *args):
        pass

    def grade(self):

        for sub in self.dirs:
            try:

                student_path = join(self.SUBMISSION, sub)
                zip_file = os.listdir(student_path)[0]
                student_ID = os.path.basename(zip_file).split("_")[0]
                print("\n====>Grading {}\n".format(student_ID))

                if os.path.exists(join(student_path, student_ID)):
                    shutil.rmtree(join(student_path, student_ID))

                with zipfile.ZipFile(join(student_path, zip_file), 'r') as zip_ref:
                    zip_ref.extractall(join(student_path, student_ID))

                if self.mode == "all":
                    tasks = sorted([task for task in os.listdir(join(
                        student_path, student_ID)) if os.path.isdir(join(student_path, student_ID, task))])
                else:
                    tasks = [task for task in os.listdir(join(
                        student_path, student_ID)) if os.path.isdir(join(student_path, student_ID, task)) and self.mode in join(student_path, student_ID, task)]

                for task in tasks:
                    if self._is_done(student_ID, task):
                        print(self.grades)
                        continue
                    task_path = join(student_path, task)

                    task_grade = self.get_grade(task, task_path, student_ID)
                    self._update_dict(student_ID, task, 1, task_grade)

            except Exception as e:

                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("ERROR student ID : {}, {} Error type : {} Error line : {}".format(
                    student_ID, e, exc_type, exc_tb.tb_lineno))
                self.grades[student_ID]["ERROR"] = e

            finally:
                shutil.rmtree(join(student_path, student_ID))
                self._update_json()

        pass
        # return grade

    def _update_dict(self, task_num, st_id, state, grade=-1):
        self.grades[st_id][task_num]['state'] = state
        self.grades[st_id][task_num]['grade'] = grade

    def _update_json(self):
        os.remove(self.OUTPUT)
        with open(self.OUTPUT, 'w') as w:
            json.dump(self.grades, w, indent=4)

        pass

    def _is_done(self, student_ID, task):
        return self.grades[student_ID][task]['state'] == DONE

    def _read_image(self, img, color=True):
        if color:
            return cv2.cvtColor(cv2.imread(img, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        else:
            return cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    def _prepare(self):
        # self.imgs = {os.path.basename(img): self.read_image(img) if 'task1_2' in img else self.read_image(
        #     img, False) for img in glob(join(self.IMG_PATH, '*'))}
        self.dirs = [submission for submission in os.listdir(
            self.SUBMISSION) if os.path.isdir(join(self.SUBMISSION, submission))]
        pass

    def _set_grades(self):
        if os.path.exists(self.OUTPUT):
            print("RESULT ALREADY EXISTS IN {}".format(self.OUTPUT))
            return
        with open(self.student_ID_List_PATH, 'r') as r:
            self.student_id_list = json.load(r)
        for id in self.student_id_list:
            self.grades[id] = {}
            d = self.grades[id]
            d['ERROR'] = ERROR
            for t in self.task_list:
                d[t] = {'state': -1}
                d[t]['grade'] = 0

        with open(self.OUTPUT, 'w') as w:
            json.dump(self.grades, w, indent=4)
        pass


if __name__ == "__main__":
    pass
