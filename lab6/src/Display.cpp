#include "Display.hpp"

void Display::show(cv::Mat frame) {
    if (!frame.empty()) {
        cv::imshow("Lab 6 - OpenCV", frame); // створює вікно 
    }
}