from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np

incDirs = ['/usr/local/include',
           '/usr/local/cuda/include',
           np.get_include()]

libDirs = ['/usr/local/lib']

setup(ext_modules=[Extension("optical_flow_wrapper", 
                             ["optical_flow_wrapper.pyx", 
                              "opt_flow.cpp"], 
                              include_dirs=incDirs,
                              library_dirs=libDirs,
                              language="c++",)],
      cmdclass = {'build_ext': build_ext})