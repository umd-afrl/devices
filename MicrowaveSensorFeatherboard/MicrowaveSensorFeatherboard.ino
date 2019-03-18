#include <WebSocketsServer.h>
#include <WiFi.h>
const char* ssid     = "NETGEAR65";
const char* password = "orangeonion830";
String state = "0";
int pbIn = 12;
WebSocketsServer webSocket = WebSocketsServer(80);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t strlength) {
  Serial.println("EVENT");
  if(digitalRead(pbIn) == HIGH){
    state = "0";
  } else{
    state = "1";
  }
  webSocket.broadcastTXT(state);
  delay(10);
}

void setup() {
  pinMode(pbIn, INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    Serial.println("ATTEMPTING TO CONNECT");
    delay(1000);
  }
  Serial.println("WIFI CONNECTED");
  Serial.println(WiFi.localIP());
  //server.begin();
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  delay(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  webSocket.loop();
}
