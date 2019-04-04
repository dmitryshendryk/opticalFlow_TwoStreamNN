import argparse

from video import demo 
from yolo import YOLO

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="main fucntion"
    )

    parser.add_argument('command', metavar='<command>', help="''")

    args = parser.parse_args()

    if args.command == 'demo':
        demo(YOLO())