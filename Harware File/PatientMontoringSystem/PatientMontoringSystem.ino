  
   /* 1) Displays user's live and changing BPM, Beats Per Minute, in Arduino's native Serial Monitor.
    2) Print: "♥  A HeartBeat Happened !" when a beat is detected, live.
    2) Learn about using a PulseSensor Library "Object".
    4) Blinks LED on PIN 13 with user's Heartbeat.
    --------------------------------------------------------------------*/
  
  #define USE_ARDUINO_INTERRUPTS true    // Set-up low-level interrupts for most acurate BPM math.
  #include <PulseSensorPlayground.h>     // Includes the PulseSensorPlayground Library.   
  
  //  Variables
  const int PulseWire = A0;       // PulseSensor PURPLE WIRE connected to ANALOG PIN 0
  const int Led = 13;         // The on-board Arduino LED, close to PIN 13. aad red  Led and buzzer on thi also
   const int bep = 11;            // it is for bep but i have set blue led on this
  int Threshold = 550;           // Determine which Signal to "count as a beat" and which to ignore.
  // Use the "Gettting Started Project" to fine-tune Threshold Value beyond default setting.
  // Otherwise leave the default "550" value.
  
  PulseSensorPlayground pulseSensor;  // Creates an instance of the PulseSensorPlayground object called "pulseSensor"
  // oximeter define code here
  #include <Wire.h>
  #include "MAX30100_PulseOximeter.h"
  
  #define REPORTING_PERIOD_MS     1000
  
  PulseOximeter pox;
  uint32_t tsLastReport = 0;
  
  void onBeatDetected()
  {
    Serial.println("Beat!");
  }
  void setup() {
  
    Serial.begin(115200);          // For Serial Monitor
  
    // Configure the PulseSensor object, by assigning our variables to it.
    pulseSensor.analogInput(PulseWire);
    pulseSensor.blinkOnPulse(Led);       //auto-magically blink Arduino's LED with heartbeat.
    pulseSensor.setThreshold(Threshold);
   
    pinMode(11, OUTPUT); // use this for bep buzzer install on baoud
  
    // Double-check the "pulseSensor" object was created and "began" seeing a signal.
    if (pulseSensor.begin()) {
      //Serial.println("");  //This prints one time at Arduino power-up,  or on Arduino reset.
    }
  
    // oximeter coder start here
    //Serial.begin(115200);
    Serial.print("Initializing pulse oximeter..");
  
    // Initialize the PulseOximeter instance
    // Failures are generally due to an improper I2C wiring, missing power supply
    // or wrong target chip
    if (!pox.begin()) {
      Serial.println("FAILED");
      for (;;);
    } else {
      Serial.println("SUCCESS");
    }
    pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
  
    // Register a callback for the beat detection
    pox.setOnBeatDetectedCallback(onBeatDetected);
  
  }
  
  void loop() {
      int j = 1;
      for (int i = 0; i < 3; i++) {
        if (j == 1) {
          int  myBPM = -1;
          // "myBPM" hold this BPM value now.
          myBPM = pulseSensor.getBeatsPerMinute();  // Calls function on our pulseSensor object that returns BPM as an "int".
          digitalWrite(bep, LOW);     //  bep off
          if (myBPM == 0)
            digitalWrite(bep, HIGH);   // bep on
          //
          if (pulseSensor.sawStartOfBeat()) {            // Constantly test to see if "a beat happened".
            Serial.print("\nA Heartbeat Happened BPM :* "); // If test is "true", print a message "a heartbeat happened".
            //Serial.print("");                        // Print phrase "BPM: "
            Serial.println(myBPM);                        // Print the value inside of myBPM.
          }
          j++;
      }
  
 
      //oximeter code start here
  
      // Make sure to call update as fast as possible
      else {
  
        pox.update();
        if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
         // int BPM=(pox.getHeartRate());
          //Serial.print("\nA Heartbeat Happened BPM :* ");
          //Serial.println(BPM);
          Serial.print(" Oxygen Level SpO2:$ ");
          Serial.println(pox.getSpO2());
          // Serial.println("%");
  
          tsLastReport = millis();
           
          }
     
          //delay(5);
        }
    }
    delay(5000);
  }
