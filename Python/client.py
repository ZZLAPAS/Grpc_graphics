from __future__ import print_function

import logging

import grpc
from protos import helloworld_pb2
from protos import helloworld_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
    print("Greeter client received: " + response.message)
    
    
class GreetClient:
    def __init__(self,channel_address='localhost:50051'):
        self.channel = grpc.insecure_channel(channel_address)  #客户端可以创建到 gRPC 服务器的连接
        self.stub = helloworld_pb2_grpc.GreeterStub(self.channel)
        
    def Send_request(self):
        self.response = self.stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
        return self.response

if __name__ == "__main__":
    logging.basicConfig()
    client = GreetClient()
    
    response = client.Send_request()
    print(response)
    #run()
