import scipy.misc as misc

import numpy as np
import numpy.linalg as la

import matplotlib.pyplot as plt
import os
import sys 

ROOT_DIR = os.path.abspath('../')


import flowfilter.plot as fplot
import flowfilter.gpu.flowfilters as gpufilter

# paths to image and ground truth data
basepath = os.path.join(ROOT_DIR, 'dataset/')
imgpath = basepath + 'test_cat.jpg'
gtpath = basepath + 'of_{0:04d}.npy'

# GPU filter object with 2 pyramid levels
gpuF = gpufilter.PyramidalFlowFilter(480, 640, 2)
gpuF.gamma = [10, 50]                                   # gains for each level
gpuF.maxflow = 4.0                                      # maximum optical flow value
gpuF.smoothIterations = [2, 4]                          # smooth iterations per level

# print('maxflow: {0}'.format(gpuF.maxflow))
offset = 100
K = 20

avgET = np.zeros(K)
images_list = os.listdir(basepath)
print(images_list.sort())
fig = plt.figure(figsize=(12,2.2)); 
fig.set_tight_layout(True)

for img_name in images_list:
    
    ##########################################
    # COMPUTATION
    ##########################################
    
    # read and load next image to the filter
    img = misc.imread(os.path.join(basepath, img_name), flatten=True).astype(np.uint8)
    img = misc.imresize(img, (480, 640))

    gpuF.loadImage(img)
    
    # compute new estimate of optical flow
    gpuF.compute()
    
    # return a Numpy ndarray with the new optical flow estimation
    flow = gpuF.getFlow()
    
    # runtime in milliseconds
    # avgET[k - offset] = gpuF.elapsedTime()
    
    
    ##########################################
    # PLOT RESULTS
    ##########################################
    
    # ground truth flow
    # flowGT = np.load(gtpath.format(k))
    
    # EndPoint error
    # epError = la.norm(flow - flowGT, axis=2)
    
    plt.subplot2grid((1,4), (0,0))
    plt.imshow(img, vmin=0, vmax=255, cmap=plt.cm.get_cmap('gray'))
    plt.title('k = {0}'.format(img_name))
    plt.colorbar()
    
    plt.subplot2grid((1,4), (0,1))
    # plt.imshow(fplot.flowToColor(flowGT, 3.0)); plt.title('Ground truth')
    
    plt.subplot2grid((1,4), (0,2))
    plt.imshow(fplot.flowToColor(flow, 3.0)); plt.title('Flow-filter')
    plt.title('k = {0}'.format(img_name))                                                             
    plt.subplot2grid((1,4), (0,3))
    # plt.imshow(epError, vmin=0, vmax=1, cmap=plt.cm.get_cmap('gray'))
    plt.title('error')
    plt.colorbar()

    plt.show()

    
print('average elapsed time: {0} ms'.format(np.average(avgET)))