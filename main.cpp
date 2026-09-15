#include <Arduino.h> // Include Arduino core library

// ============================
// Arduino Stepper Control for ZeGa Actuator Deployment
// ---------------------------------------------------------------
// Using DRV8825 Stepper Driver with Acxico 2-Phase 4-Wire Planetary Stepper Motor
// ============================

// ============================
// Pin Definitions
// ============================
#define STEP_PIN 2    // Pin for step pulses
#define DIR_PIN 3     // Pin for direction control (CW/CCW)
#define ENABLE_PIN 4  // Pin to enable/disable motor driver (LOW = enabled)

// ============================
// Movement Parameters
// ============================
int step_A = 500;  // First forward movement steps
int delay_A = 3000; // Pause after first movement (ms)
int step_B = 800;  // Second forward movement steps
int delay_B = 5000; // Pause after second movement (ms)

// ============================
// Setup: Configure Arduino Pins
// ============================
void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  // Enable the stepper driver (LOW = enabled, HIGH = disabled)
  digitalWrite(ENABLE_PIN, LOW);

  Serial.begin(9600); // Enable serial monitor
  Serial.println("Actuator System Ready.");
}

// ============================
// Function to Move Stepper Motor
// ============================
void moveStepper(int steps, bool dir, int speedMicros = 1000) {
  /*
  Moves the stepper motor in the desired direction.
  - steps: Number of steps to move.
  - dir: Direction (true = CW, false = CCW).
  - speedMicros: Delay between steps in microseconds.
  */
  digitalWrite(DIR_PIN, dir); // Set rotation direction
  
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(speedMicros);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(speedMicros);
  }
}

// ============================
// Actuator Deployment Sequence
// ============================
void loop() {
    if (Serial.available()) {
      String input = Serial.readStringUntil('\n');
      int aIndex = input.indexOf("A=");
      int bIndex = input.indexOf("B=");
  
      if (aIndex != -1 && bIndex != -1) {
        int commaIndex = input.indexOf(',');
        int a = input.substring(aIndex + 2, commaIndex).toInt();
        int b = input.substring(bIndex + 2).toInt();
  
        Serial.println("Actuator Triggered!");
        Serial.print("Step A = ");
        Serial.print(a);
        Serial.print(", Step B = ");
        Serial.println(b);
  
        Serial.print("Moving out ");
        Serial.print(a);
        Serial.println(" steps...");
        moveStepper(a, true);
        delay(3000);
  
        Serial.print("Moving out ");
        Serial.print(b);
        Serial.println(" steps...");
        moveStepper(b, true);
        delay(5000);
  
        Serial.print("Retracting ");
        Serial.print(a + b);
        Serial.println(" steps...");
        moveStepper(a + b, false);
  
        Serial.println("Actuator Deployment Complete.\n");
      }
    }
  }  