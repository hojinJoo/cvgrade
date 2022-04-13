import importlib
import sys


path = "/mnt/c/Users/hj/Desktop/downloads/CV_project1/BAE,WOOJIN-2018147546_6130510_assignsubmission_file_/2018147546_project1/task1"
sys.path.append(path)


mod = importlib.import_module(
    'denoise', '.'.join(path.split('/')))
task1_2 = getattr(mod, 'task1_2')

task1_2('./project1/test_images/task1_2_1_noise.jpg',
        './project1/test_images/task1_2_1_clean.jpg', './result.jpg')
sys.path.pop()


del sys.modules['denoise']
path = "/mnt/c/Users/hj/Desktop/downloads/CV_project1/CHOI,HYUKJIN-2016147516_6130540_assignsubmission_file_/2016147516_project1/2016147516_project1/task1"
sys.path.append(path)


mod = importlib.import_module(
    'denoise', '.'.join(path.split('/')))
task1_2 = getattr(mod, 'task1_2')

task1_2('./project1/test_images/task1_2_1_noise.jpg',
        './project1/test_images/task1_2_1_clean.jpg', './result.jpg')
