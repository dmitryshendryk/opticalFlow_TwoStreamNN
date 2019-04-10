
#ifndef GRANDPARENT_H
#define GRANDPARENT_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include <string>
#include <vector>
#include <math.h>
#include <iostream>
#include <fstream>
#include <sys/time.h>
#include <time.h>
#include <sstream>

#include <QDirIterator>
#include <QFileInfo>
#include <QString>

#include <opencv2/core/core.hpp>
#include "opencv2/video/tracking.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/cuda.hpp"
#include "opencv2/cudaoptflow.hpp"

#include <dirent.h>

#define N_CHAR 500
#define WRITEOUT_IMGS 1

using namespace std;
using namespace cv;
using namespace cv::cuda;

namespace pre_process 
{

    float MIN_SZ = 256;
    float OUT_SZ = 256;

    bool clipFlow = true; // clips flow to [-20 20]
    bool resize_img = false;

    // These are default paths

   
    bool createOutDirs = true;

    /* THESE ARE MY PARAMS, NOT FEICHENHOFER'S */

    bool debug = false;
    bool rgb = false;
    bool bins = false;

    // Global variables for cuda::BroxOpticalFlow
    const float alpha_ = 0.197;
    const float gamma_ = 50;
    const float scale_factor_ = 0.8;
    const int inner_iterations_ = 10;
    const int outer_iterations_ = 77;
    const int solver_iterations_ = 10;

    const int RESIZE_WIDTH = 224;
    const int RESIZE_HEIGHT = 224;
    const bool warp = false;

    int vidcount = 0;

    class OpticalFlow 
    {
        public:
            GpuMat frame0GPU, frame1GPU, flowGPU;
            Mat frame0_rgb_, frame1_rgb_, frame0_rgb, frame1_rgb, frame0, frame1, rgb_out;
            Mat frame0_32, frame1_32, imgU, imgV;
            Mat motion_flow, flow_rgb;
            Mat flowCPU, planes[3], mag;
            char cad[N_CHAR];
            struct timeval tod1;
            double t1 = 0.0, t2 = 0.0, tdflow = 0.0, t1fr = 0.0, t2fr = 0.0, tdframe = 0.0;



            OpticalFlow();
            ~OpticalFlow();

            void convertFlowToImage(const Mat &flowIn, Mat &flowOut,
		                float lowerBound, float higherBound);
            int compute_Flow(int start_with_vid, int gpuID, int type, int frameSkip,
                        String vid_path, String out_path, String out_path_jpeg);
    };
}

#endif