

import csv 
import numpy as np 
import sys 
import os 
import cv2
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical


ROOT_DIR = os.path.abspath('./')

class DatasetOptical():

    def __init__(self):
        pass 
    

    def get_capture(self,cap,type,filename, write_csv=False):
        
        w = int(cap.get(3))
        h = int(cap.get(4))
        if type == 'rgb':
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        elif type == 'optical':
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(filename, fourcc, 15, (w, h))

        if write_csv:
            list_file = open('detection.txt', 'w')
            frame_index = -1
            out.write(frame)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')

        return out
    
        

    def generate_dataset_video(self, class_type, frame, opt_frame, counter, folder_name):
        os.makedirs(os.path.join(ROOT_DIR + '/dataset/train/' + class_type , folder_name), exist_ok=True)
        os.makedirs(os.path.join(ROOT_DIR + '/dataset/train/' + class_type + '/' + folder_name , 'opt_flow'), exist_ok=True)
        os.makedirs(os.path.join(ROOT_DIR + '/dataset/train/' + class_type + '/' + folder_name , 'frames'), exist_ok=True)
        

        os.makedirs(os.path.join(ROOT_DIR + '/dataset/test/' + class_type, folder_name), exist_ok=True)
        os.makedirs(os.path.join(ROOT_DIR + '/dataset/test/'  + class_type + '/' + folder_name , 'opt_flow'), exist_ok=True)
        os.makedirs(os.path.join(ROOT_DIR + '/dataset/test/'  + class_type + '/' + folder_name , 'frames'), exist_ok=True)
        
        if counter % 10 == 0:
            cv2.imwrite(os.path.join(ROOT_DIR + '/dataset/test/' + class_type + '/' + folder_name + '/frames'  , "frame%d.jpg" % counter), frame)
            cv2.imwrite(os.path.join(ROOT_DIR + '/dataset/test/' + class_type + '/' + folder_name + '/opt_flow'  , "optical%d.jpg" % counter), opt_frame)
        else:
            cv2.imwrite(os.path.join(ROOT_DIR + '/dataset/train/' + class_type + '/' + folder_name + '/frames'  , "frame%d.jpg" % counter), frame)
            cv2.imwrite(os.path.join(ROOT_DIR + '/dataset/train/' + class_type + '/' + folder_name + '/opt_flow'  , "optical%d.jpg" % counter), opt_frame)

        list_file = open(os.path.join(ROOT_DIR + '/dataset', 'data_list.csv') , 'w')
        list_file.write("train," +"accidents,"+ str(folder_name)+',' + str(300))