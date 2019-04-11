
cdef extern from "opt_flow.hpp" namespace "pre_process":
    cdef cppclass OpticalFlow:
        OpticalFlow();
        
        int compute_Flow(int start_with_vid, int gpuID, int type, int frameSkip,
                        str vid_path, str out_path, str out_path_jpeg);
    cdef cppclass GpuMat:
        GpuMat frame0GPU, frame1GPU, flowGPU;
    
    cdef cppclass Mat:
        Mat frame0_rgb_, frame1_rgb_, frame0_rgb, frame1_rgb, frame0, frame1, rgb_out;
        Mat frame0_32, frame1_32, imgU, imgV;
        Mat motion_flow, flow_rgb;
        Mat flowCPU, planes[3], mag;
    
    char cad[500];
    double t1 = 0.0, t2 = 0.0, tdflow = 0.0, t1fr = 0.0, t2fr = 0.0, tdframe = 0.0;

    


cdef class PyOpticalFlow:
    cdef OpticalFlow *thisptr;

    def __cinit__(self):
        self.thisptr = new OpticalFlow();
    
    def compute_Flow(self, start_with_vid, gpuID, type, frameSkip, vid_path,  out_path,  out_path_jpeg):
        return self.thisptr.compute_Flow(start_with_vid, gpuID, type, frameSkip, vid_path,  out_path,  out_path_jpeg)
    
