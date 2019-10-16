#include <Motor.h>
#include <Colin.h>
#include "HX711.h"
#include <ContinuousServo.h>
#include <Filters.h>
#include <SimpleKalmanFilter.h>
#include <Stream.h>
HX711 scale(A3, A2);
float read_ADC;
float read_load;
// HX711.DOUT  - pin #A3
// HX711.PD_SCK - pin #A2

float offset = 0;
float initial_reading;
float estimated_value;
int flag = 0;
// create servo object to control a servo 

//Adjust Last Parameter for measurement rate
SimpleKalmanFilter simpleKalmanFilter(3, 3, 0.1);

// filters out noise with frequency larger than 5 Hz.
float filterFrequency = 5.0  ;
// create a one pole (RC) lowpass filter
FilterOnePole lowpassFilter( LOWPASS, filterFrequency );   


void setup() {
    Serial.begin(115200); 
    scale.set_scale(450.0f);
    delay(500);
    scale.tare();


}

void loop() {
     
 while(!Serial.available())
 { 
  
  read_load = scale.get_units();

  estimated_value= simpleKalmanFilter.updateEstimate(read_load);
 if(estimated_value<= -10){
    offset = -1* (estimated_value/2);
    estimated_value = 0;
  }
  estimated_value += offset;

  
  Serial.println(estimated_value);
  Serial.flush();
  }
  char input_value = Serial.read();
  if(input_value == '0'){
    scale.tare();
  }


  
}
