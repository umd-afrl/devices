#include <WebSocketsServer.h>
#include <WiFi.h>
const char* ssid     = "NETGEAR65";
const char* password = "orangeonion830";
bool state = false;
int pbIn = 12;
int ledPin = 13;
WebSocketsServer webSocket = WebSocketsServer(80);

// |  ||
// || |_

void setup() {
  pinMode(ledPin, OUTPUT);
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
  //webSocket.onEvent(webSocketEvent);
  delay(1000);
}

void loop() {
  state = false;
  for(int i = 0; i < 100; i++){
    if(state != true){
      state = !digitalRead(pbIn);
    }
    delay(1);
  }
  if(state){
    webSocket.broadcastTXT("1");
    digitalWrite(ledPin, HIGH);
  } else {
    webSocket.broadcastTXT("0");
    digitalWrite(ledPin, LOW);
  }
  webSocket.loop();
}
