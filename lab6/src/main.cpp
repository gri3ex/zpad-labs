#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    // створює об'єкти наших класів
    CameraProvider camera(0); // 0 - індекс стандартної камери
    KeyProcessor keyHandler;
    FrameProcessor processor;
    Display viewer;

    Mode currentMode = Mode::ORIGINAL;

    // Головний цикл програми
    while (true) {
        // 1. отримує кадр
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        // 2. обробляє кадр відповідно до обраного режиму
        cv::Mat processedFrame = processor.process(frame, currentMode);

        // 3. відображає результат
        viewer.show(processedFrame);

        // 4. отримує натиснуту клавішу
        int key = cv::waitKey(30);
        
        // вихід 
        if (key == 27) break;

        // оновлює режим обробки
        currentMode = keyHandler.getMode(key, currentMode);
    }

    return 0;
}