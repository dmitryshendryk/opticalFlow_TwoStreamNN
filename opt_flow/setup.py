from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension("optical_flow_wrapper", 
                             ["optical_flow_wrapper.pyx", 
                              "opt_flow.cpp"], 
                              libraries=['Qt5Widgets', 'OpenCV'],
                              language="c++",)],
      cmdclass = {'build_ext': build_ext})