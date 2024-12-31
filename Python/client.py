from __future__ import print_function

import logging

import grpc
from protos import helloworld_pb2
from protos import helloworld_pb2_grpc

import matplotlib.pyplot as plt
import numpy as np
import re
    
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
    
    plt.ion()  # 打开交互模式
    fig, ax = plt.subplots()
    x_data, y_data = [], []  # 用于存储曲线数据
    line, = ax.plot(x_data, y_data, label="Response Value")

    # 图表设置
    ax.set_xlim(0, 50)  # x 轴范围
    ax.set_ylim(-1, 1)   # y 轴范围（根据 response 数据调整）
    ax.set_xlabel("Time")
    ax.set_ylabel("Response")
    ax.set_title("Real-time Response Plot")
    ax.legend()
    
    i = 1;
    while(1):
        response = client.Send_request()
        print(response)
        
        numbers = re.findall(r'-?\d+\.\d+', str(response))
        
        x_data.append(i)
        i = i+1
        y_data.append(numbers)
        
        # 更新数据
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        
        # 动态调整 x 轴范围
        if i > 50:  # 当数据超过 50 时，向右滚动
            ax.set_xlim(i - 50, i)
        
        current_ylim = ax.get_ylim()    
        if float(numbers[0]) > current_ylim[1]:  # 当数据超过 50 时，向右滚动
            ax.set_ylim(current_ylim[0],current_ylim[1]+1)
        if float(numbers[0]) < current_ylim[0]:  # 当数据超过 50 时，向右滚动
            ax.set_ylim(current_ylim[0]-1,current_ylim[1])
        
        
        # 刷新图表
        plt.pause(0.01)  # 暂停 0.1 秒用于绘图
        fig.canvas.draw()

    plt.ioff()  # 关闭交互模式
    plt.show()
    #run()
