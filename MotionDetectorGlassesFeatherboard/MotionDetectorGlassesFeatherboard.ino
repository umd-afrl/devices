#include <WebSocketsClient.h>
#include <WiFi.h>
const char* ssid     = "NETGEAR65";
const char* password = "orangeonion830";

int ledPin = 13;
WebSocketsClient websocket;

void websocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_CONNECTED:
      Serial.printf("[WSc] Connected to url: %s\n", payload);

      // send message to server when Connected
      websocket.sendTXT("Connected");
      break;
    case WStype_TEXT:
      if(strcmp((char *) payload, "1")){
        digitalWrite(ledPin, LOW);
      }
      else{
        digitalWrite(ledPin, HIGH);
      }
      websocket.sendTXT("OK");

      // send message to server
      // webSocket.sendTXT("message here");
      break;
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("ATTEMPTING TO CONNECT");
    delay(1000);
  }
  websocket.begin("192.168.1.12", 80, "/");
  websocket.onEvent(websocketEvent);
  websocket.setReconnectInterval(100);
}

void loop(){
  websocket.loop();
}
