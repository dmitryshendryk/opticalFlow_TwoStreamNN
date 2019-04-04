import argparse

from video import demo 
from yolo import YOLO
from two_stream_network.spatial_train import train_spatial
from two_stream_network.temporal_train import train_temporal 

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="main fucntion"
    )

    parser.add_argument('command', metavar='<command>', help="''")

    args = parser.parse_args()

    if args.command == 'demo':
        demo(YOLO(), True)
    

    if args.command == 'train_spatial':
        train_spatial()
    
    if args.command == 'train_temporal':
        train_temporal() 

