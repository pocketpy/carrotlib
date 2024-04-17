cmake_minimum_required(VERSION 3.10)

project(naett)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

include_directories(${CMAKE_SOURCE_DIR}/include)

aux_source_directory(${CMAKE_SOURCE_DIR}/src SRC_LIST)

add_library(${PROJECT_NAME} STATIC ${SRC_LIST})
