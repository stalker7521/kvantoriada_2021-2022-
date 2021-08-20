#include <SoftwareSerial.h>
#include <Servo.h>
#define rx 8
#define tx 9

#define SPEED_1      5 
#define DIR_1        4
#define SPEED_2      6
#define DIR_2        7

int pwm_speed = 255;
int in;
char info;
bool count = 0;

SoftwareSerial mySerial = SoftwareSerial(rx, tx);

Servo servo;     


void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);

 for (int i = 4; i < 8; i++) {     
  pinMode(i, OUTPUT);
  }
    
  
  pinMode(12, OUTPUT);
 
  servo.attach(12);  
  servo.write(86); 
  
}

void loop() {

  if(Serial.available()){
    info = char(Serial.read());
    switch (info){
     case '4':
       primo();
       break;
     case '2':
       leva();
       break;
     case '3':
       neva();
       break;
     case '1':
       go();
       break;
     case 'r':
       revers();
       break;
     case '0':
       stopend();
       break;
  }
 }
 else
  if (mySerial.available()){
    info = char(mySerial.read());
    switch (info){
     case 'p':
       primo();
       break;
     case 'l':
       leva();
       break;
     case 'n':
       neva();
       break;
     case 'g':
       go();
       break;
     case 'r':
       revers();
       break;
     case 's':
       stopend();
       break;
    }  
  }
}

void primo (){
  servo.write(90); 
  
}

void leva (){
  servo.write(115); 
  
}

void neva (){
    servo.write(65); 

}


void go (){
  digitalWrite(DIR_1, LOW);
  analogWrite(SPEED_1, 255);
  digitalWrite(DIR_2, LOW);
  analogWrite(SPEED_2, 255);
  
}

void revers (){
  digitalWrite(DIR_1, HIGH);
  analogWrite(SPEED_1, 255);
  digitalWrite(DIR_2, HIGH);
  analogWrite(SPEED_2, 255);
  
}

void stopend (){
   analogWrite(SPEED_1, 0);
   analogWrite(SPEED_2, 0);
}
