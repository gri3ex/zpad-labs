cmake_minimum_required(VERSION 3.10)
project(Lab7_OpenCV)

set(CMAKE_CXX_STANDARD 17)
set(OpenCV_DIR "C:/opencv/build")

find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED) # підключення потоків

include_directories(${OpenCV_INCLUDE_DIRS} include)
file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(lab7_exe ${SOURCES})
target_link_libraries(lab7_exe ${OpenCV_LIBS} Threads::Threads)