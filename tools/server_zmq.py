import zmq
import sys
import threading
import time
from random import randint, random
import json

import cv2 
import numpy as np 

__author__ = "Felipe Cruz <felipecruz@loogica.net>"
__license__ = "MIT/X11"

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = u'worker-%d' % self.id
        socket.identity = identity.encode('ascii')
        socket.connect('tcp://localhost:5570')
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            print('Req #%d sent..' % (reqs))
            socket.send_string(u'request #%d' % (reqs))
            for i in range(5):
                sockets = dict(poll.poll(1000))
                if socket in sockets:
                    msg = socket.recv()
                    tprint('Client %s received: %s' % (identity, msg))

        socket.close()
        context.term()

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(5):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        tprint('Worker started')
        counter = 1
        while True:
            counter += 1 
            ident, msg = worker.recv_multipart()
            img=[]
            for byte in msg:
                img.append(byte)
            
            img = np.array(img,dtype=np.uint8)
            img = img.reshape(640,1240,1)
            
            # print(l.shape)
            # cv2.imshow("frame", l)
            # cv2.waitKey(0)
            cv2.imwrite("/home/dmitry/Documents/Projects/opticalFlow_TwoStreamNN/dataset/py_res/img_" + str(counter) + '.jpg', img)
            print('Worker received {} from {}'.format(img, ident))
            replies = randint(0,4)
            for i in range(replies):
                time.sleep(1. / (randint(1,10)))
                worker.send_multipart([ident, msg])

        worker.close()

if __name__ == '__main__':

    server = ServerTask()
    server.start()