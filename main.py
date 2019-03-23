import os 
import sys 
import argparse
from train_t3d import run_train
from samples.video_demo import run_video

ROOT_DIR = os.path.abspath('./')
sys.path.append(ROOT_DIR)


DEFAULT_TXT = './train.list'
DEFAULT_VIDEO = './val_dataset/videos/basketball.avi'


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='Accident detection'
    )

    parser.add_argument('command', metavar='<command>')
    parser.add_argument('--list', required=False,
                        default=DEFAULT_TXT,
                        type=str,
                        metavar="/path/to/list/",
                        help='Training data (default=list/)')
    
    parser.add_argument('--video', required=False,
                        default=DEFAULT_VIDEO,
                        type=str,
                        metavar="/path/to/list/",
                        help='Training data (default=list/)')

    args = parser.parse_args()

    if args.command == 'train_t3d':
        run_train(args.list)
    
    if args.command == 'video_detect':
        run_video(args.video)
        

    
    

