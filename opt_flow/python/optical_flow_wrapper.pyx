
from libcpp.string cimport string

cdef extern from "<opencv2/videoio/videoio.hpp>" namespace "cv": 
    cdef cppclass VideoCapture: 
        pass 

cdef extern from "../opt_flow.hpp" namespace "pre_process":
    cdef cppclass OpticalFlow:
        OpticalFlow();

        int compute_Flow(int start_with_vid, int gpuID, int type, int frameSkip,
                        string vid_path, string out_path, string out_path_jpeg, VideoCapture cap);


cdef class PyOpticalFlow:
    cdef OpticalFlow *thisptr;

    def __cinit__(self):
        self.thisptr = new OpticalFlow();
    
    def compute_Flow(self, start_with_vid, gpuID, type, frameSkip, vid_path,  out_path,  out_path_jpeg):
        return self.thisptr.compute_Flow(start_with_vid, gpuID, type, frameSkip, vid_path,  out_path,  out_path_jpeg, cap)
    
