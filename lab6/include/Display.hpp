#pragma once
#include <opencv2/opencv.hpp>

class Display {
public:
    // відображає результат у вікні 
    void show(cv::Mat frame);
};