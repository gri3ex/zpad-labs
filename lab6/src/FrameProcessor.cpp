#include "FrameProcessor.hpp"

cv::Mat FrameProcessor::process(cv::Mat frame, Mode mode) {
    cv::Mat result;
    if (mode == Mode::GRAY) {
        cv::cvtColor(frame, result, cv::COLOR_BGR2GRAY);
    } else if (mode == Mode::CANNY) {
        cv::Canny(frame, result, 50, 150); // Фільтр Кенні
    } else if (mode == Mode::BLUR) {
        cv::GaussianBlur(frame, result, cv::Size(15, 15), 0); // Розмиття 
    } else {
        result = frame.clone(); // Оригінал 
    }
    return result;
}