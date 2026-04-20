#pragma once
#include <opencv2/opencv.hpp>

class CameraProvider {
public:
    // відкриває камеру
    CameraProvider(int deviceId = 0);
    // Метод для отримання нового кадру
    cv::Mat getFrame();
private:
    cv::VideoCapture cap;
};