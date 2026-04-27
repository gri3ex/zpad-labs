#pragma once

// список режимів обробки
enum class Mode {
    ORIGINAL,
    GRAY,
    CANNY,
    BLUR
};

class KeyProcessor {
public:
    // метод, що повертає режим залежно від натиснутої клавіші 
    Mode getMode(int key, Mode currentMode);
};
