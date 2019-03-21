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


def compute_accuracy(logit,labels):
    correct=tf.equal(tf.argmax(logit,1),labels)
    acc=tf.reduce_mean(tf.cast(correct,tf.float32))
    return acc

#Cell for Testing!
BATCH_SIZE=1
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
    
    acc=compute_accuracy(logit,label_placeholder)
    init=tf.global_variables_initializer()
    saver=tf.train.Saver(tf.global_variables())
    
    config=tf.ConfigProto()
    gpu_options = tf.GPUOptions(allow_growth=True)
    sess = tf.Session()  
    sess.run(init)
   
    saver.restore(sess,'./weights/T3DBN_TFCKPT_ITER_4999-4999')
    print('Start Testing.')
    
    print('l={}'.format(testloader.len//BATCH_SIZE))
    resacc=0
    c=0
    for step in range(testloader.len//BATCH_SIZE):
        
        
        test_images,test_labels,_=testloader.next_batch()
        print(test_images[0].shape)
        curacc=sess.run(acc,feed_dict={
                        input_placeholder:test_images,
                        label_placeholder:test_labels})
        print(curacc)
        resacc+=curacc
        c+=1
    print('Accuracy:{:.2f}'.format(resacc/c))   
            