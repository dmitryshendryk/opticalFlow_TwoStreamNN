from distutils.core import setup, find_packages
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension("optical_flow_wrapper", 
                             ["optical_flow_wrapper.pyx", 
                              "opt_flow.cpp"], 
                              libraries=['Qt5Widgets', 'OpenCV'],
                              packages = find_packages(),
                              language="c++",)],
      cmdclass = {'build_ext': build_ext})