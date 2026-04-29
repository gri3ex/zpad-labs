#include <opencv2/opencv.hpp>
#include <iostream>
#include "../include/FaceDetector.hpp"

int main() {
    cv::VideoCapture cap(0); // відкриває камеру
    if (!cap.isOpened()) {
        std::cerr << "Помилка: не вдалося відкрити камеру!" << std::endl;
        return -1;
    }

    FaceDetector faceDetector;
    bool faceMode = false; // режим детекції вимкнено за замовчуванням
    cv::Mat frame;

    std::cout << "Управління:\n 'f' - увімкнути/вимкнути пошук обличчя\n 'Esc' - вихід" << std::endl;

    while (true) {
        cap >> frame; // читає кадр з камери
        if (frame.empty()) break;

        if (faceMode) {
            // відправка копії кадру у фоновий потік
            faceDetector.setFrame(frame);

            // координати та прямокутники
            std::vector<cv::Rect> faces = faceDetector.getFaces();
            for (const auto& face : faces) {
                cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2); // Зелена рамка
            }
            cv::putText(frame, "Face Detection: ON (Multithreaded)", cv::Point(10, 30), 
                        cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 255, 0), 2);
        } else {
            cv::putText(frame, "Face Detection: OFF (Press 'f')", cv::Point(10, 30), 
                        cv::FONT_HERSHEY_SIMPLEX, 0.7, cv::Scalar(0, 0, 255), 2);
        }

        cv::imshow("Lab 7 - CV & Multithreading", frame);

        // Обробка клавіш
        char key = (char)cv::waitKey(1);
        if (key == 27) { // Клавіша Esc
            break;
        } else if (key == 'f' || key == 'F') { // Клавіша F
            faceMode = !faceMode;
        }
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;
}