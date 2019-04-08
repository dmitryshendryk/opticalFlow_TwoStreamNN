import argparse

from video import demo 
from yolo import YOLO
from two_stream_network.spatial_train import train_spatial
from two_stream_network.temporal_train import train_temporal 
from two_stream_network.fuse_validate import fuse_train


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="main fucntion"
    )

    parser.add_argument('command', metavar='<command>', help="''")
    parser.add_argument('--spatial')
    parser.add_argument('--temporal')


    args = parser.parse_args()

    if args.command == 'demo':
        demo(YOLO(), True)
    

    if args.command == 'train_spatial':
        train_spatial()
    
    if args.command == 'train_temporal':
        train_temporal() 
    
    if args.command == 'train_fuse':
        fuse_train(args.spatial, args.temporal)

