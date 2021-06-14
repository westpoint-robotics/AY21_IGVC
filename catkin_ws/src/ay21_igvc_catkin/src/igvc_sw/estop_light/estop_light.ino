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

const int blinkSigPin = 4; // Relay for light
const int wireless = 8;
const int wired = A0;

unsigned long previousMillis = 0; 
const long interval = 500;
int ledState = LOW;

//void blinkLight( const std_msgs::Int8& light_State){
//  if (light_State.data == 2){
//  digitalWrite(blinkSigPin, HIGH);   // signal other Arduino to blink the led
//  }
//  else {
//    digitalWrite(blinkSigPin, LOW); //keep the arduino on while teleop or manual
//  }
//}

void blinkLight( const std_msgs::Int8& light_State){
  Serial.println(light_State.data);
  if (light_State.data == 2){
    //doBlink();   // signal other Arduino to blink the led
    Serial.println("Change this");
  }
}

ros::Subscriber<std_msgs::Int8> sub("/gem/operation_mode", &blinkLight );
std_msgs::Bool bool_msg;
ros::Publisher Estop("gem/eStop", &bool_msg);

void setup()
{
  Serial.begin(57600);
  pinMode(blinkSigPin, OUTPUT);
  pinMode(wired, INPUT);
  pinMode(wireless, INPUT);
  digitalWrite(blinkSigPin, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);
  digitalWrite(blinkSigPin, LOW);   // turn the LED on (HIGH is the voltage level)

  nh.initNode();
  nh.subscribe(sub);
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

void doBlink()
{
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    // if the LED is off turn it on and vice-versa:
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }

    // set the LED with the ledState of the variable:
    digitalWrite(blinkSigPin, ledState);
  }
}

bool buttonSurvey(){ 
  Serial.println(digitalRead(wired));
  if (digitalRead(wireless) || analogRead(wired) > 100){
    doBlink();
    return true;
  }
  else{
    return false;
  }
}
