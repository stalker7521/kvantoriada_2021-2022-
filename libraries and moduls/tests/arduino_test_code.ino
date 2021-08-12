#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3); // RX, TX
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  mySerial.begin(9600);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
}

// the loop function runs over and over again forever
void loop() {
  if (Serial.available()){
    char info = Serial.read();
    mySerial.print(info);
    digitalWrite(LED_BUILTIN, HIGH);
    }
}
