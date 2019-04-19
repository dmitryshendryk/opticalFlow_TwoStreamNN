#ifndef ZMQCLIENT
#define ZMQCLIENT

#include <vector>
#include <thread>
#include <memory>
#include <functional>

#include <zmq.hpp>
#include <zhelpers.hpp>

#include <vector>
#include <opencv2/core/core.hpp>
#include "opencv2/highgui/highgui.hpp"

//  This is our client task class.
//  It connects to the server, and then sends a request once per second
//  It collects responses as they arrive, and it prints them out. We will
//  run several client tasks in parallel, each with a different random ID.
//  Attention! -- this random work well only on linux.

using namespace cv;

class client_task {
public:
    client_task();
    void start();
    Mat pImg_U;
    Mat pImg_V;

private:
    zmq::context_t ctx_;
    zmq::socket_t client_socket_;
};

//  Each worker task works on one request at a time and sends a random number
//  of replies back, with random delays between replies:
#endif