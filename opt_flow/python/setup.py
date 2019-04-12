from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np


import os 
import sysconfig


incDirs = ['/usr/local/include',
           '/home/dmitry/Qt/5.9/gcc_64/include',
           '/usr/local/cuda/include',

           np.get_include()]

libDirs = ['/usr/local/lib', '/home/dmitry/Qt/5.9/gcc_64/lib']

cflags = ['-std=c++11']


def get_ext_filename_without_platform_suffix(filename):
    name, ext = os.path.splitext(filename)
    ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')

    if ext_suffix == ext:
        return filename

    ext_suffix = ext_suffix.replace(ext, '')
    idx = name.find(ext_suffix)

    if idx == -1:
        return filename
    else:
        return name[:idx] + ext


class BuildExtWithoutPlatformSuffix(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        return get_ext_filename_without_platform_suffix(filename)




setup(ext_modules=[Extension(name="cOptical", 
                             sources=["optical_flow_wrapper.pyx", 
                              "../opt_flow.cpp"], 
                              include_dirs=incDirs,
                              library_dirs=libDirs,
                              language="c++",
                              extra_compile_args=cflags)],
      cmdclass = {'build_ext': BuildExtWithoutPlatformSuffix})