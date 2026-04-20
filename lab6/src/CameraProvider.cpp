#include "CameraProvider.hpp"

// конструктор: відкриває камеру за вказаним ID (0 - зазвичай вбудована)
CameraProvider::CameraProvider(int deviceId) {
    cap.open(deviceId);
}

// метод для захоплення одного кадру
cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame; // записує дані з камери в матрицю
    return frame;
}