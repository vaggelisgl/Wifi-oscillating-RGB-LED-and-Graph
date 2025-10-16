#include <WiFiS3.h>
#include "secrets.h"
WiFiUDP udp;
#define port 12345
#include <Wire.h>
#include <SPI.h>
String stringArray[10];
String mystring;
int l=0,u=255;
void setup() {
 pinMode(3,OUTPUT);
 pinMode(5,OUTPUT);
 pinMode(10,OUTPUT);
 Serial.begin(9600);
  Serial.print("connecting to ");
  Serial.println(mySSID);
  WiFi.begin(mySSID,myPASS);
  while(WiFi.status()!=WL_CONNECTED){
    delay(100);
    Serial.print(".");

  }
Serial.println("\nConnected to Wifi");
while(WiFi.localIP() == IPAddress(0,0,0,0)){
  Serial.println(WiFi.localIP());
}
Serial.println(WiFi.localIP());
udp.begin(port);
Serial.print("udp set to port ");
Serial.println(port);
}

void loop() {
  if(udp.parsePacket()){
    mystring=udp.readStringUntil('\n');
    splitString();
    analogWrite(3,stringArray[0].toInt());
    analogWrite(5,stringArray[1].toInt());
    analogWrite(10,stringArray[2].toInt());
   }}

    void splitString() {
mystring=mystring+":";
int i=0;
int start=0;
int indexCount=0;
for(int i=0;i<mystring.length();i++){
  if(mystring[i]==':'){
    stringArray[indexCount]=mystring.substring(start,i);
    indexCount++; start=i+1;
  }
}}
