#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

// Змінна для перемикання режимів обробки
int currentMode = 0; 

// 3. Реагування на мишу: Функція зворотного виклику
void onMouseAction(int event, int x, int y, int flags, void* userdata) {
    if (event == EVENT_LBUTTONDOWN) {
        cout << "Клік миші: x=" << x << ", y=" << y << endl;
    }
}

int main() {
    // 1. Читання відео з камери
    VideoCapture videoSource(0); 
    if (!videoSource.isOpened()) {
        cerr << "Помилка: Камеру не знайдено!" << endl;
        return -1;
    }

    string winName = "Lab 6: OpenCV Interactive";
    namedWindow(winName);

    // Встановлює обробник миші для вікна
    setMouseCallback(winName, onMouseAction);

    Mat rawFrame, displayFrame;

    cout << "Керування: 1-Оригінал, 2-Сірий, 3-Canny, 4-Blur, Esc-Вихід" << endl;

    // Основний цикл програми
    while (true) {
        videoSource >> rawFrame; // Читаю кадр
        if (rawFrame.empty()) break;

        // 4. Режими обробки зображень залежно від клавіш
        if (currentMode == 1) {
            cvtColor(rawFrame, displayFrame, COLOR_BGR2GRAY); // Сірий
        } else if (currentMode == 2) {
            Canny(rawFrame, displayFrame, 50, 150); // Межі
        } else if (currentMode == 3) {
            GaussianBlur(rawFrame, displayFrame, Size(15, 15), 0); // Розмиття
        } else {
            displayFrame = rawFrame.clone(); // Оригінал
        }

        // 2. Відображення у вікні
        imshow(winName, displayFrame);

        // 3. Реагування на клавіатуру
        char pressedKey = (char)waitKey(30);
        if (pressedKey == 27) break; // Esc
        if (pressedKey == '1') currentMode = 0;
        if (pressedKey == '2') currentMode = 1;
        if (pressedKey == '3') currentMode = 2;
        if (pressedKey == '4') currentMode = 3;
    }

    videoSource.release();
    destroyAllWindows();
    return 0;
}