/*
 *
 * Copyright 2015 gRPC authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include <iostream>
#include <memory>
#include <string>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "absl/strings/str_format.h"

#include <grpcpp/ext/proto_server_reflection_plugin.h>
#include <grpcpp/grpcpp.h>
#include <grpcpp/health_check_service_interface.h>

#ifdef BAZEL_BUILD
#include "examples/protos/helloworld.grpc.pb.h"
#else
#include "helloworld.grpc.pb.h"
#endif

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using helloworld::Greeter;
using helloworld::HelloReply;
using helloworld::HelloRequest;

ABSL_FLAG(uint16_t, port, 50051, "Server port for the service");

// Logic and data behind the server's behavior.
class GreeterServiceImpl final : public Greeter::Service {             //继承.proto文件中的Greeter，，，：：Service则是proto Buffer生成的C++代码中的生成的类对应.proto文件中的service
  Status SayHello(ServerContext* context, const HelloRequest* request,          //SayHello是.proto文件中定义的客户端请求服务的名称
                  HelloReply* reply) override {                                 //HelloRequest是.proto文件中定义的请求服务消息包的名称，并在生成的C++代码中是一个类，通过形参request操作
                                                                                //HelloReply是服务器将返回给客户端的   Response 消息包名称

    std::string prefix("Hello ");
    reply->set_message(prefix + request->name());  //request->name() 获取客户端请求中的名字
    return Status::OK;
  }
};

void RunServer(uint16_t port) {
  std::string server_address = absl::StrFormat("0.0.0.0:%d", port);
  GreeterServiceImpl service;

  grpc::EnableDefaultHealthCheckService(true);
  grpc::reflection::InitProtoReflectionServerBuilderPlugin();
  ServerBuilder builder;
  
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());       //将构建的服务器绑定到指定的地址和端口
  
  builder.RegisterService(&service);                                             //将之前创建的 GreeterServiceImpl 实例注册为 gRPC 服务
  
  std::unique_ptr<Server> server(builder.BuildAndStart());                       //使用 BuildAndStart() 方法构建并启动服务器，并返回一个指向 Server 对象的智能指针，当有端口有请求出现，调用回应函数
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  RunServer(absl::GetFlag(FLAGS_port));
  return 0;
}
