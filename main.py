import argparse
from project1 import Grader_task1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default='all')
    args = parser.parse_args()

    a = Grader_task1(args.mode)
    a.grade()
    # a.grade()
