import tensorflow as tf
import numpy as np
import os
import random
import PIL.Image as Image
import cv2
import os
import copy
import time
from T3D import inference_t3d
import DataGenerator
from settings import *
from videocaptureasync import WebcamVideoStream, FPS
from multiprocessing import Queue, Pool


ROOT_DIR = os.path.abspath('./')

def compute_accuracy(logit,labels):
    correct=tf.equal(tf.argmax(logit,1),labels)
    acc=tf.reduce_mean(tf.cast(correct,tf.float32))
    return acc

#Cell for Testing!
BATCH_SIZE=1
classes = ['Basketball playing', 'playing piano']
#Essential:set 'IS_TRAIN' -> False
IS_TRAIN=False
testloader=DataGenerator.DataGenerator(filename='test.list',
                                batch_size=BATCH_SIZE,
                                num_frames_per_clip=NUM_FRAMES_PER_CLIP,
                                shuffle=False,is_da=False)
tf.reset_default_graph()
print('IS_TRAIN:',IS_TRAIN)
print('KEEP_PROB:',KEEP_PROB)
USE_PRETRAIN=True
# MODEL_PATH='./GT_TFCKPT_ITER_3000-3000'
with tf.Graph().as_default():
    global_step=tf.get_variable('global_step',[],initializer=tf.constant_initializer(0),trainable=False)
    input_placeholder=tf.placeholder(tf.float32,shape=[BATCH_SIZE,NUM_FRAMES_PER_CLIP,CROP_SIZE,CROP_SIZE,3])
    label_placeholder=tf.placeholder(tf.int64,shape=[BATCH_SIZE])

    logit=inference_t3d(input_placeholder)
    
    # acc=compute_accuracy(logit,label_placeholder)
    init=tf.global_variables_initializer()
    saver=tf.train.Saver(tf.global_variables())
    
    config=tf.ConfigProto()
    gpu_options = tf.GPUOptions(allow_growth=True)
    sess = tf.Session()  
    sess.run(init)
   
    saver.restore(sess,'./weights/T3DBN_TFCKPT_ITER_4999-4999')
    print('Start Testing.')

    cap = cv2.VideoCapture(os.path.join(ROOT_DIR,'val_dataset/videos/basketball.avi'))
    
    # def worker(input_q, output_q):
    # # Load a (frozen) Tensorflow model into memory.
    #     detection_graph = tf.Graph()
    #     with detection_graph.as_default():
    #         od_graph_def = tf.GraphDef()
    #         with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    #             serialized_graph = fid.read()
    #             od_graph_def.ParseFromString(serialized_graph)
    #             tf.import_graph_def(od_graph_def, name='')

    #         sess = tf.Session(graph=detection_graph)
    #     fps = FPS().start()
    #     while True:
    #         fps.update()
    #         frame = input_q.get()
    #         x_batch = np.expand_dims(batch, axis=0)
    #         curacc=sess.run(logit,feed_dict={input_placeholder:x_batch})
    #         output_q.put(curacc)
    #         print(curacc)
    #     fps.stop()
    #     sess.close()


    # input_q = Queue(maxsize=16)
    # output_q = Queue(maxsize=16)
    # pool = Pool(2, worker, (input_q, output_q))


    # cap = WebcamVideoStream(os.path.join(ROOT_DIR,'play_piano.avi'),640,480).start()
    # fps = FPS().start()

    batch = []
    while True:
        ret, frame = cap.read()
        # print(frame)
        if ret == True:
        # if cap.grabbed == True:
            frame = cv2.resize(frame, (160, 160))
            batch.append(frame)
            if len(batch) == 16:
                x_batch = np.expand_dims(batch, axis=0)
                curacc=sess.run(logit,feed_dict={input_placeholder:x_batch})
                detected_class = np.argmax(curacc)
                probability = max(curacc[0])
                print(curacc)
                print("{} : {:.2f} %".format(classes[detected_class],probability * 100))
                batch.clear()
            cv2.imshow('frame', frame)
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
        else:
            break
    # fps.stop()
    # cap.stop()
    cap.release()
    cv2.destroyAllWindows()

            