#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import os
from timeit import time
import warnings
import sys
import cv2
import numpy as np
from PIL import Image
from yolo import YOLO

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
warnings.filterwarnings('ignore')


from scipy import misc 

ROOT_DIR = os.path.abspath('./')
sys.path.append(ROOT_DIR)

import flowfilter.plot as fplot
import flowfilter.gpu.flowfilters as gpufilter

from src.dataset import DatasetOptical


def demo(yolo, createDataset_flag=False):

    datasetOptical = DatasetOptical()

   # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0

    gpuF = gpufilter.PyramidalFlowFilter(480, 640, 2)
    gpuF.gamma = [10, 50]                                   # gains for each level
    gpuF.maxflow = 4.0                                      # maximum optical flow value
    gpuF.smoothIterations = [2, 4]                          # smooth iterations per level
    
   # deep_sort 
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)
    
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    writeVideo_flag = False 
    
    video_capture = cv2.VideoCapture('/home/dmitry/Documents/Projects/deep_sort_yolov3/dataset/YoutubeVid1.mp4')


    dt = DatasetOptical()

    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1 
        
    fps = 0.0
    count = 0
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        if ret != True:
            break
        t1 = time.time()
        frame_flow = frame.copy()

       # image = Image.fromarray(frame)
        image = Image.fromarray(frame[...,::-1]) #bgr to rgb
        boxs = yolo.detect_image(image)
       # print("box_num",len(boxs))
        features = encoder(frame,boxs)
        
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        
        # Call the tracker
        tracker.predict()
        tracker.update(detections)
        
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(track.track_id),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)

        for det in detections:
            bbox = det.to_tlbr()
            cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)
        
        cv2.namedWindow("Optical flow", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
        # Compute optical flow 
        img = cv2.cvtColor(frame_flow, cv2.COLOR_BGR2GRAY)
        img = misc.imresize(img, (480, 640))
        gpuF.loadImage(img)
        gpuF.compute()
        flow = gpuF.getFlow()

        # rgb_frame_out.write(frame)
        opt_flow = fplot.flowToColor(flow, 3.0)
        
        # optical_frame_out.write(opt_flow)
        # cv2.imwrite("frame%d.jpg" % count, frame)
        # cv2.imwrite("optical_frame%d.jpg" % count, opt_flow)

        if createDataset_flag:
            dt.generate_dataset_video( 'no_accidents', frame, opt_flow, count, '0001')

        
        cv2.imshow("Optical flow", fplot.flowToColor(flow, 3.0))
        cv2.imshow('Tracking', frame)
        count += 1
        if writeVideo_flag:
            # save a frame
            out.write(frame)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')
            
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        print("fps= %f"%(fps))
        
        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    # rgb_frame_out.release()
    # optical_frame_out.release()
    
    if writeVideo_flag:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(YOLO())