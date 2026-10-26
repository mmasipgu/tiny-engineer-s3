#pragma once
#include <cstdint>

// I2C: PCA9685 + SSD1306
constexpr int I2C_SDA = 8;
constexpr int I2C_SCL = 9;

// I2S: MAX98357A
constexpr int I2S_BCLK = 17;
constexpr int I2S_LRC = 18;
constexpr int I2S_DIN = 21;

// RGB status LED (change at build time if needed)
#ifndef TE_RGB_PIN
#define TE_RGB_PIN 48
#endif
constexpr int RGB_LED_PIN = TE_RGB_PIN;

// PCA9685 OE, active LOW
constexpr bool PCA9685_OE_WIRED = true;
constexpr int PCA9685_OE_PIN = 16;

// GPIO19/20 intentionally reserved for native USB D-/D+

constexpr int SAMPLE_RATE = 22050;

constexpr uint8_t PCA9685_ADDRESS = 0x40;
constexpr int SERVO_STEP_MS = 10;
constexpr float SERVO_BOOT_SPEED_DEG_S = 35.0f;
constexpr int SERVO_MIN_US = 800;
constexpr int SERVO_MAX_US = 2200;

constexpr int OLED_WIDTH = 128;
constexpr int OLED_HEIGHT = 32;
constexpr uint8_t OLED_ADDRESS = 0x3C;
