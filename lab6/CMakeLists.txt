cmake_minimum_required(VERSION 3.10)
project(Lab6_OpenCV)

set(CMAKE_CXX_STANDARD 17)
set(OpenCV_DIR "C:/opencv/build")

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS} include)

file(GLOB_RECURSE SOURCES "src/*.cpp" "main.cpp")

add_executable(lab6_exe ${SOURCES})

target_link_libraries(lab6_exe ${OpenCV_LIBS})
