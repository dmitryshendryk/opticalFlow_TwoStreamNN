from distutils.core import setup
from distutils.extension import Extension

import numpy as np


import os 
import sysconfig


incDirs = ['/usr/local/include',
           '/usr/local/cuda/include',
           np.get_include()]

libDirs = ['/usr/local/lib']

cflags = ['-std=c++11']



setup(ext_modules=[Extension(name="cOptical", 
                             sources=[ "optpy.cpp", "../opt_flow_img.cpp"], 
                             libraries=['boost_python-py35', 'opencv_contrib', 'opencv_core', 
                             'opencv_features2d', 'opencv_flann','opencv_gpu','opencv_highgui', 'opencv_imgproc',
                              'opencv_legacy','opencv_ml', 'opencv_objdetect','opencv_ocl', 'opencv_photo',
                              'opencv_stitching', 'opencv_superres', 'opencv_ts', 'opencv_video', 'opencv_videostab'],
                              include_dirs=incDirs,
                              library_dirs=libDirs,
                              language="c++",
                              extra_compile_args=cflags)])