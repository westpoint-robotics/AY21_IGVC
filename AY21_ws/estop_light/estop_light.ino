/*
 * rosserial Subscriber Example
 * Blinks an LED on callback
 */

#include <ros.h>
#include <Arduino.h>

#include <std_msgs/Empty.h>
#include <std_msgs/Int8.h>
#include <std_msgs/Bool.h>

ros::NodeHandle nh;

//int blinkSigPin = 9; // connects to the second arduino.
const int wireless = 7;
const int wired = 8;

//void blinkLight( const std_msgs::Int8& light_State){
//  if (light_State.data == 2){
//  digitalWrite(blinkSigPin, HIGH);   // signal other Arduino to blink the led
//  }
//  else {
//    digitalWrite(blinkSigPin, LOW); //keep the arduino on while teleop or manual
//  }
//}

//ros::Subscriber<std_msgs::Int8> sub("/gem/operation_mode", &blinkLight );
std_msgs::Bool bool_msg;
ros::Publisher Estop("gem/eStop", &bool_msg);

void setup()
{
  Serial.begin(57600);
  //pinMode(blinkSigPin, OUTPUT);
  pinMode(wired, INPUT);
  pinMode(wireless, INPUT);
  nh.initNode();
  //nh.subscribe(sub);
  nh.advertise(Estop);
}

void loop()
{  
  bool_msg.data = buttonSurvey();
  Serial.println(bool_msg.data);
  nh.spinOnce();
  Estop.publish(&bool_msg);
    delay(100);
}

bool buttonSurvey(){
  if (digitalRead(wireless) || digitalRead(wired)){
    return true;
  }
  else{
    return false;
  }
}
