#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    // обробляє кадр відповідно до обраного режиму
    cv::Mat process(cv::Mat frame, Mode mode);
};