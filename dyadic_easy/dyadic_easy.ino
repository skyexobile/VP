#include <Servo.h>
#include <Motor.h>
#include <Colin.h>
#include <Encoder.h>
#include "HX711.h"
#include <Filters.h>
#include <SimpleKalmanFilter.h>
HX711 scale;
bool strong;
float read_ADC;
float read_load;
bool printed;
int sp_flag;
int received_val;
// HX711.DOUT  - pin #A3
// HX711.PD_SCK - pin #A2
bool init_flag = true;
float previous_steps;
#define ENC_A 2
#define ENC_B 3
#define ENC_PORT PIND
uint8_t bitShift = 2; // change to suit your pins (offset from 0,1 per port)
// Note: You need to choose pins that have Interrupt capability.
bool adjust_flag = false;
bool loosen_flag = false;
int counter = 0;
boolean ticToc;
float initial_reading;
float estimated_value;
bool first_reading = true;
char receivedChar;
int steps;
bool reset;
#define outputA 5
#define outputB 4
float SP_soft, SP_med, SP_hard;
int counter2 = 0;
int aState;
int aLastState;
char mode;
Servo servo;
int setPoint;
bool readjust, set_flag, stop_squeeze;
bool loosening;
//Adjust Last Parameter for measurement rate
SimpleKalmanFilter simpleKalmanFilter(3, 3, 0.1);
bool flush_val, flush_val2;
// filters out noise with frequency larger than 5 Hz.
float filterFrequency = 5.0;
// create a one pole (RC) lowpass filter
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );   
float offset;
float range;
float input_val;
float Output;

void setup() {
  strong = false;
  reset = false;
  sp_flag = 0;
  loosening = false;
  Serial.begin(115200); 
  servo.attach(6);
   servo.write(90);

  //servo.write(70);
  //delay(1500);
  scale.begin(A3, A2);
  scale.set_scale(-435.5f);
  delay(300);
  scale.tare();
  delay(200);

  pinMode(ENC_A, INPUT);
  digitalWrite(ENC_A, HIGH);
  pinMode(ENC_B, INPUT);
  digitalWrite(ENC_B, HIGH);
  counter = 0;
  ticToc = false;
  offset = 0;
  // Attach ISR to both interrupts

  SP_soft = 80;
  SP_med = 90;
  SP_hard = 100;
  pinMode(outputA, INPUT);
  pinMode(outputB, INPUT);
  aLastState = digitalRead(outputA);
  mode = 'n';
  setPoint = 0;
  readjust = false;
  set_flag = false;
  steps = 90;
  stop_squeeze =false;
  flush_val = false;
  flush_val2 = false;
 scale.tare();
}

void loop() {


 while(!Serial.available()){ //not reading anything
  //amplifier stuff
 
    read_load = scale.get_units();

  input_val = -1 * simpleKalmanFilter.updateEstimate(read_load);
  if(input_val <= -10){
    offset = -1* (input_val/2);
    input_val = 0;
  }
  input_val = input_val + offset;

  

    

  if(setPoint !=0 && loosening == false){
  //  Serial.println("doing stuff because there's a set point");
   // Serial.println(setPoint);
       read_load = scale.get_units();
  input_val = -1* simpleKalmanFilter.updateEstimate(read_load);
         //Serial.println(input_val);
         input_val = input_val + offset;


  
    if(setPoint>=300){
      range = setPoint/10;
    }
    else{
      range = 1;
    }
    if(loosening == false && setPoint !=0 && (setPoint - input_val) <= 5 && input_val>=setPoint){
  //Serial.println("stopping");
  //Serial.println("something is happening here");
  steps = 90;
  servo.write(steps);
  //delay(500);
  //steps = 98;
  //servo.write(steps);
  Serial.println("adjusting");
    if(strong){
      //delay(1480);
      strong = false;
    }
    else{
    //delay(1300);
    Serial.println("adjusting2");
    }
   // servo.write(90);
  
    flush_val = true;

    }


    //readjust affecting speed. 
/*
    if(readjust == false){
      if((input_val - setPoint) > range){
        Output = 94;//loosen
        Serial.println("loosen");
      }
      else if(input_val - setPoint < -1*range){
        Output = 83; //tighten
        Serial.println("tighten");
      }
      else{
        Output = 90;
        readjust = true;
      }
    }
    else{ //readjust is true
       if(input_val-setPoint > range){
      //Loosen
      Output = 93;
     Serial.println("readjust loosen");
    }
    else if(input_val - setPoint < -1*range){
      //Tighthen
      Output = 82;
      Serial.println("readjust tighten");
    }
    else{
      //within acceptable range
      Output = 90;
    }
  }

    servo.write(Output);
    
      
    }

  if(adjust_flag){
    //Serial.println("begin adjusting");
    servo.write(84);

    if(counter >=0){
      servo.write(90);
      adxust_flag = false;
      //Serial.println("finish adjusting");
    }
  }
 
    */
  }
        // Serial.println(input_val);

 }


 //Serial.read() ensures fast reading
  received_val = Serial.read();
  Serial.println(received_val);
switch(received_val){
  //finding weak SP = 'a' ->97
  case 97:
    steps = 83;
    sp_flag = 1;
    loosening = false;
    break;
  //findindg medium SP = 'b' -> 98
  case 98:
    steps = 83;
    sp_flag = 2;
    loosening = false;
    break;
  //finding hard SP = 'c' -> 99
  case 99:
    steps = 83;
    sp_flag = 3;
    loosening = false;
    break;

//reset sensor = r ->114
  
  case 114:
    reset=true;
     steps = 90;
     break;  
   case 115: //emergency stop s= 115
    
    servo.write(90);
     steps = 90;
     setPoint = 0;    
     break;
  


    
  //weak 1 = 'A' -> 65
  case 65:
    steps = 82;
    setPoint = SP_soft;
    loosening = false;
    flush_val = true;  
    break;
   //weak 2 = 'B' -> 66
  case 66:
   steps = 80;
   setPoint = SP_soft;
   loosening = false;
   flush_val = true;  
   break;

  //weak 3 = 'C' -> 67
  case 67:
     steps = 78;
     setPoint = SP_soft;
     loosening = false;
     flush_val = true;  
     break;
  
  //medium 1 = 'D' -> 68
  case 68:
   steps = 78;
   setPoint = SP_med;
   loosening = false;
   flush_val = true;  
   break;

  //medium 2 = 'E' -> 69
  case 69:
   steps = 76;
   setPoint = SP_med;
   loosening = false;
   flush_val = true;  
   break;

  //medium 3 = 'F' -> 70
  case 70:
   steps = 74;
   setPoint = SP_med;
   loosening = false;
   flush_val = true;  
   break;

  //strong 1 = 'G' ->71
  case 71:
  strong = true;
   steps = 74;
   setPoint = SP_hard;
   loosening = false;
   flush_val = true;  
   break;

  //strong 2 = H' -> 72
  case 72:
  strong = true;
    steps = 72;
    setPoint = SP_hard;
    loosening = false;
    flush_val = true;
    break;

  //strong 3 = I - > 73
  case 73:
  strong = true;
    steps = 70;
    setPoint = SP_hard;
    loosening = false;
    flush_val = true;
    break;

  //burst of realease = J -> 74
  case 74:
    servo.write(99);
    delay(850);
    setPoint = 0;
    flush_val = true;
    break;
    //continuous release = K -> 75
  case 75:
    
    switch(sp_flag){
      case 1:
        SP_soft = input_val;
        //Serial.println("soft point is ");
        //Serial.println(SP_soft);
        break;
      case 2:
        SP_med = input_val;
       //Serial.println("medium point is ");
        //Serial.println(SP_med);
        break;
      case 3:
        SP_hard = input_val;
        strong = true;
        //Serial.println("hard point is ");
        //Serial.println(SP_hard);
        break;
    }
    sp_flag = 0;
    steps = 97;
    reset=true;
    /*if (strong){
      delay(1480);
      strong = false;
    }
    else{
    delay(1200);
    }*/
    flush_val = true;
    loosening = true;
    loosen_flag= true;
           //Serial.print("here loosen flag is: ");
      // Serial.println(loosen_flag);

    break;
  //reset = L -> 76
  case 76:
   servo.write(75);
   delay(600);
   steps = 90;
   setPoint = 0;
   break;
   //readjust by tightening M == 77
  case 77:
    servo.write(82);
    delay(900);
    steps = 90;
    setPoint = 0;
    flush_val = true;
    break;
      //print setpoints = Z

  
}



read_load = scale.get_units();

  input_val= simpleKalmanFilter.updateEstimate(read_load);
   if(input_val <= -10){
    offset = -1* (input_val/2);
    input_val = 0;
  }
  
  input_val = input_val + offset;
if(loosening == false && setPoint !=0 && (setPoint - input_val) <= 5 && input_val>=setPoint){
  //Serial.println("stopping2");
  steps = 90;
}

  servo.write(steps);
  //int micro = servo.readMicroseconds();
 // Serial.println(micro);

   if (loosen_flag){
    if(setPoint == SP_hard){
      delay(2300);
    }
    else if (setPoint == SP_med){
    delay(1700);
    }
    else{
      delay(1000);
    }
    servo.write(90);
      Serial.println("stopping2");
          steps=90;
          setPoint = 0;
    flush_val = true;

    loosen_flag = false;
    loosening=false;
    delay(200);
    scale.tare();
    }
     if(reset){
    delay(200);
    scale.tare();
    reset = false;
  }
  /*if(flush_val){
    Serial.println("1");
    flush_val = !flush_val;
  }
*/


  }
 
