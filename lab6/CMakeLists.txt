cmake_minimum_required(VERSION 3.10)
project(ZPAD_Lab6)

set(CMAKE_CXX_STANDARD 17)

# Пошук встановленої бібліотеки OpenCV
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# Створення виконваного файлу
add_executable(lab6_exe src/main.cpp)

# Лінкування OpenCV
target_link_libraries(lab6_exe ${OpenCV_LIBS})
