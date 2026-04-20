#include "../include/FaceDetector.hpp"
#include <chrono>

FaceDetector::FaceDetector() : running(true), newFrameAvailable(false) {
    net = cv::dnn::readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    workerThread = std::thread(&FaceDetector::worker, this);
}

FaceDetector::~FaceDetector() {
    running = false;
    if (workerThread.joinable()) {
        workerThread.join();
    }
}

void FaceDetector::setFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    currentFrame = frame.clone();
    newFrameAvailable = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return detectedFaces;
}

void FaceDetector::worker() {
    while (running) {
        cv::Mat frameForInference;
        bool process = false;

        {
            std::lock_guard<std::mutex> lock(mtx);
            if (newFrameAvailable) {
                frameForInference = currentFrame.clone();
                newFrameAvailable = false;
                process = true;
            }
        }

        if (process && !frameForInference.empty()) {
            cv::Mat blob = cv::dnn::blobFromImage(frameForInference, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
            net.setInput(blob);
            cv::Mat detections = net.forward();

            // штучне навантаження
            std::this_thread::sleep_for(std::chrono::milliseconds(500));

            std::vector<cv::Rect> newFaces;
            cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

            for (int i = 0; i < detectionMat.rows; i++) {
                float confidence = detectionMat.at<float>(i, 2);
                if (confidence > 0.5) { // Впевненість > 50%
                    int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameForInference.cols);
                    int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameForInference.rows);
                    int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameForInference.cols);
                    int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameForInference.rows);
                    newFaces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
                }
            }

            {
                std::lock_guard<std::mutex> lock(mtx);
                detectedFaces = newFaces;
            }
        } else {
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }
}