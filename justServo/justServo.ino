#include <Servo.h>
Servo servo;
void setup() {

  Serial.begin(115200); 
  servo.attach(6);
  servo.write(90);

}

void loop() {

 //Serial.read() ensures fast reading
 if (Serial.available()){
  int val = Serial.parseInt();
       
       if(val != 0){

   servo.write(val);
   Serial.println(val);
   }
 }

}
