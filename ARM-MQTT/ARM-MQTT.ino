// Certs and Credentials
#include "certs.h"
// Basic MQTT and WiFi Libraries
#include <MQTT.h>
#include <WiFi.h>

// MQTT Definitions
#define ESP_getChipId()   ((uint32_t)ESP.getEfuseMac())
#define DEVICE_NAME "ESPDev001"

// Control Definitions
#define Claw 5
#define Wrist 25
#define Elbow 26
#define Shoulder 27
#define Base 14

#define vcc 32
#define vee 33

WiFiClient net;
MQTTClient client = MQTTClient(256);

void messageReceived(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);
  if (topic == "/efe") {
    FmoveP();
    Fmove();
    Fmove();
    Fmove();
    FmoveR();
  }
  else if (topic == "/al") {
    SmoveP();
    Smove();
    Smove();
    Smove();
    SmoveR();
  }
  else if (topic == "/ef") {
    TmoveP();
    Tmove();
    Tmove();
    Tmove();
    TmoveR();
  }
}

void setup() {
  Serial.begin(115200);
  controlSetup();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  client.onMessage(messageReceived);
  connect();
  client.publish("/test", string2char("Hello World"));
  client.subscribe("/efe");
  client.subscribe("/al");
  client.subscribe("/ef");
}

void loop() {
  client.loop();
  if (!client.connected()) {
    connect();
  }
}

char* string2char(String command) {
  if (command.length() != 0) {
    char *p = const_cast<char*>(command.c_str());
    return p;
  }
}

void connectToWiFi() {
  int conCounter = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    conCounter++;
    if (conCounter == 10) {
      ESP.restart();
    }
  }
  Serial.println("");
  Serial.println("Connected to WiFi");
}

void connectToMQTT()
{
  client.begin(ENDPOINT, 1883, net);
  while (!client.connect(DEVICE_NAME, user, pass)) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("Connected to MQTT");
  // Make sure that we did indeed successfully connect to the MQTT broker
  // If not we just end the function and wait for the next loop.
  if (!client.connected()) {
    connect();
  }

}

void connect() {
  connectToWiFi();
  connectToMQTT();
}

void controlSetup() {
  pinMode(vcc, OUTPUT);
  pinMode(vee, OUTPUT);
  pinMode(Claw, OUTPUT);
  pinMode(Wrist, OUTPUT);
  pinMode(Elbow, OUTPUT);
  pinMode(Shoulder, OUTPUT);
  pinMode(Base, OUTPUT);
  digitalWrite(vee, HIGH);
  digitalWrite(vcc, HIGH);
  digitalWrite(Claw, HIGH);
  digitalWrite(Wrist, HIGH);
  digitalWrite(Elbow, HIGH);
  digitalWrite(Shoulder, HIGH);
  digitalWrite(Base, HIGH);
  delay(1000);
}

void VccMove(int pin, int tm) {
  digitalWrite(vee, HIGH);
  delay(50);
  digitalWrite(Claw, HIGH);
  digitalWrite(Wrist, HIGH);
  digitalWrite(Elbow, HIGH);
  digitalWrite(Shoulder, HIGH);
  digitalWrite(Base, HIGH);
  delay(50);
  digitalWrite(pin, LOW);
  digitalWrite(vcc, LOW);
  delay(tm);
  digitalWrite(vcc, HIGH);
  delay(50);
}

void VeeMove(int pin, int tm) {
  digitalWrite(vcc, HIGH);
  delay(50);
  digitalWrite(Claw, LOW);
  digitalWrite(Wrist, LOW);
  digitalWrite(Elbow, LOW);
  digitalWrite(Shoulder, LOW);
  digitalWrite(Base, LOW);
  delay(50);
  digitalWrite(pin, HIGH);
  digitalWrite(vee, LOW);
  delay(tm);
  digitalWrite(vee, HIGH);
  delay(25);
  digitalWrite(Claw, HIGH);
  digitalWrite(Wrist, HIGH);
  digitalWrite(Elbow, HIGH);
  digitalWrite(Shoulder, HIGH);
  digitalWrite(Base, HIGH);
  delay(50);
}

void FmoveP(void)
{
  VeeMove(Shoulder, 5000);
  VeeMove(Elbow, 5500);
}
void Fmove(void)
{
  VccMove(Wrist, 3500);
  VeeMove(Wrist, 3500);
}
void FmoveR(void)
{
  VccMove(Shoulder, 5500);
  VccMove(Elbow, 5500);
}

void SmoveP(void)
{
  VccMove(Base, 6000);
  VeeMove(Shoulder, 5200);
  VeeMove(Elbow, 5200);
}
void Smove(void)
{
  VccMove(Elbow, 5800);
  VeeMove(Elbow, 5200);
}
void SmoveR(void)
{
  VccMove(Elbow, 6000);
  VccMove(Shoulder, 5200);
  VeeMove(Base, 6000);

}

void TmoveP(void)
{
  VccMove(Base, 6300);
  VeeMove(Shoulder, 5000);
  VccMove(Elbow, 3000);
  VccMove(Wrist, 3500);
}
void Tmove(void)
{
  VccMove(Elbow, 4000);
  VeeMove(Elbow, 4000);
  VccMove(Elbow, 4000);
  VeeMove(Elbow, 4000);
}
void TmoveR(void)
{
  VeeMove(Elbow, 3500);
  VeeMove(Wrist, 3500);
  VccMove(Shoulder, 5700);
  VeeMove(Base, 6300);
}
