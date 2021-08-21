#include <SoftwareSerial.h>
#include <Servo.h>
#define rx 8
#define tx 9

byte ena = 3;
byte in1 = 4;
byte in2 = 5;


int in;
char info;
bool count = 0;

//SoftwareSerial mySerial = SoftwareSerial(rx, tx);

Servo servo;     


void setup() {
  Serial.begin(9600);
  //mySerial.begin(9600);

 for (int i = 4; i < 8; i++) {     
  pinMode(i, OUTPUT);
  }

  pinMode( ena, OUTPUT );
  pinMode( in1, OUTPUT );
  pinMode( in2, OUTPUT );
  
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
     case '3':
       right();
       break;
     case '2':
       left();
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
 /*
 else{
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
*/
}

void primo (){
  servo.write(90); 
  
}

void right (){
  servo.write(115); 
  
}

void left (){
    servo.write(65); 

}


void go (){
  analogWrite( ena, 255 );
  digitalWrite( in1, HIGH  );
  digitalWrite( in2, LOW );
}

void revers (){
  analogWrite( ena, 255 );
  digitalWrite( in1, LOW  );
  digitalWrite( in2, HIGH );
  
}

void stopend (){
  analogWrite( ena, 0 );
  digitalWrite( in1, LOW  );
  digitalWrite( in2, LOW );
}
