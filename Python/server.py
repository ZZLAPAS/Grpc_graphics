from concurrent import futures
import logging

import grpc
from protos import helloworld_pb2
from protos import helloworld_pb2_grpc

import threading
import time

i = 0

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message="Hello%d, %s!" %(i, request.name))


def serve():
    #port = "50051"
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port("127.0.0.1:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    thread1 = threading.Thread(target=serve)
    thread1.start()
    
    
    while(1):
        i = i+1
        time.sleep(1)
        if i == 5:
            i = 0
        print(i)
        
    thread1.join()
            
            
        
