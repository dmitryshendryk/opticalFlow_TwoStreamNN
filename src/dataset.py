

import csv 
import numpy as np 
import sys 
import os 
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import to_categorical


class DatasetOptical():

    def __init__():
        pass 
    

    def get_capture(self, cap, filename, write_csv=False):
        
        w = int(cap.get(3))
        h = int(cap.get(4))
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