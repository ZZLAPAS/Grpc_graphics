# Copyright 2018 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# cmake build file for C++ helloworld example.
# Assumes protobuf and gRPC have been installed using cmake.
# See cmake_externalproject/CMakeLists.txt for all-in-one cmake build
# that automatically builds all the dependencies before building helloworld.

cmake_minimum_required(VERSION 3.8)

project(HelloWorld C CXX)

include(common.cmake)

include_directories(${CMAKE_SOURCE_DIR}/include)
#########################################------------------------------generate file------------------------------------------------#########################################

# Proto file
get_filename_component(hw_proto "/home/mhz/TEST/gRPC_test/C++/protos/helloworld.proto" ABSOLUTE)   #将.proto文件路径装到hw_proto
get_filename_component(hw_proto_path "${hw_proto}" PATH)            #将路径提取出来

# Generated sources
set(hw_proto_srcs "/home/mhz/TEST/gRPC_test/C++/protos/helloworld.pb.cc")    #${CMAKE_CURRENT_BINARY_DIR} 是 CMake 的一个内置变量
set(hw_proto_hdrs "/home/mhz/TEST/gRPC_test/C++/protos/helloworld.pb.h")
set(hw_grpc_srcs "/home/mhz/TEST/gRPC_test/C++/protos/helloworld.grpc.pb.cc")
set(hw_grpc_hdrs "/home/mhz/TEST/gRPC_test/C++/protos/helloworld.grpc.pb.h")
add_custom_command(                                                            #add_custom_command 来生成特定的源文件和头文件
      OUTPUT "${hw_proto_srcs}" "${hw_proto_hdrs}" "${hw_grpc_srcs}" "${hw_grpc_hdrs}"    #输出文件列表
      COMMAND ${_PROTOBUF_PROTOC}               #_PROTOBUF_PROTOC为protoc 的默认可执行文件路径，代表 Protocol Buffers 编译器 (protoc) 的可执行文件
      ARGS --grpc_out "/home/mhz/TEST/gRPC_test/C++/protos"
        --cpp_out "/home/mhz/TEST/gRPC_test/C++/protos"
        -I "${hw_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${hw_proto}"
      DEPENDS "/home/mhz/TEST/gRPC_test/C++/protos")

# Include generated *.pb.h files
include_directories("/home/mhz/TEST/gRPC_test/C++/protos")

# hw_grpc_proto
add_library(hw_grpc_proto
  ${hw_grpc_srcs}
  ${hw_grpc_hdrs}
  ${hw_proto_srcs}
  ${hw_proto_hdrs})

#########################################------------------------------generate file------------------------------------------------#########################################


target_link_libraries(hw_grpc_proto
  absl::check
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})


  # Targets greeter_[async_](client|server)
foreach(_target                            #foreach 循环语句，它会遍历括号中的每个目标名称，并将每次迭代的值赋给 _target 变量
greeter_client greeter_server
)
add_executable(${_target} "${_target}.cc")
target_link_libraries(${_target}
  hw_grpc_proto
  absl::check
  absl::flags
  absl::flags_parse
  absl::log
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})
endforeach()
