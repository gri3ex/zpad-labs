#include "KeyProcessor.hpp"

Mode KeyProcessor::getMode(int key, Mode currentMode) {
    if (key == '1') return Mode::ORIGINAL;
    if (key == '2') return Mode::GRAY;
    if (key == '3') return Mode::CANNY;
    if (key == '4') return Mode::BLUR;
    return currentMode; // Якщо інша клавіша — лишає поточний режим
}