#include <zmq_client.hpp>

//  This is our client task class.
//  It connects to the server, and then sends a request once per second
//  It collects responses as they arrive, and it prints them out. We will
//  run several client tasks in parallel, each with a different random ID.
//  Attention! -- this random work well only on linux.



client_task::client_task()
        : ctx_(1),
          client_socket_(ctx_, ZMQ_DEALER)
    {}

void client_task::start() {
    // generate random identity
    char identity[10] = {};
    sprintf(identity, "%04X-%04X", within(0x10000), within(0x10000));
    // printf("%s\n", identity);
    client_socket_.setsockopt(ZMQ_IDENTITY, identity, strlen(identity));
    client_socket_.connect("tcp://localhost:5570");
    zmq::pollitem_t items[] = {{static_cast<void *>(client_socket_), 0, ZMQ_POLLIN, 0}};
    int request_nbr = 0;
    try {
        while (true) {
            for (int i = 0; i < 100; ++i) {
                // 10 milliseconds
                zmq::poll(items, 1, 10);
                if (items[0].revents & ZMQ_POLLIN) {
                    // printf("\n%s ", identity);
                    s_dump(client_socket_);
                }
            }
            
            // cv::Mat img= imread("/home/dmitry/Documents/Projects/opticalFlow_TwoStreamNN/dataset/output_x/frame000001.jpg",1);
            std::cout << "pImg_V  " <<  this->pImg_V.rows << this->pImg_V.cols << this->pImg_V.channels()  << std::endl;
            std::cout << "pImg_U  " << this->pImg_U.rows << this->pImg_U.cols << this->pImg_U.channels()  << std::endl;

            
            // client_socket_.send(img.data, img.rows*img.cols*img.channels());
            std::cout << strlen(reinterpret_cast<char const *>(this->pImg_V.data)) << std::endl;
            // std::cout << strlen(reinterpret_cast<char const *>(this->pImg_U.data)) << std::endl;
            client_socket_.send(this->pImg_V.data, this->pImg_V.rows*this->pImg_V.cols*this->pImg_V.channels());
        }
    }
    catch (std::exception &e) {}
}

//  Each worker task works on one request at a time and sends a random number
//  of replies back, with random delays between replies:
