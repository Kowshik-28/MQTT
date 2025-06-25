// Include the standard WiFi library for ESP32
#include <WiFi.h>
#include <ArduinoMqttClient.h>


const char* ssid = "Iotit";      
const char* password = "Sweety@1234"; 


WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);


const char* broker = "broker.emqx.io"; //test.mosquitto.org broker.emqx.io
const int   port   = 1883;


const char* topic   = "rj1";

char messageBuffer[10]; 


const long interval = 8000;
unsigned long previousMillis = 0;

int valueToSend = 0;

void setup() {
  Serial.begin(115200);

  while (!Serial) {
    ;
  }

  Serial.println("Starting ESP32 MQTT Client...");

  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1) {
      delay(1000);
    }
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();
}

void loop() {
  mqttClient.poll();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    valueToSend = (valueToSend + 10) % 256; 
    sprintf(messageBuffer, "%d", valueToSend);

    Serial.print("Sending message to topic: ");
    Serial.println(topic);
    Serial.print("Message content: "); // Added clarity
    Serial.println(messageBuffer);

    mqttClient.beginMessage(topic, true, 0); // topic, retain=true, qos=0
    mqttClient.print(messageBuffer);         // Send the dynamically created string
    mqttClient.endMessage();

    Serial.println();
  }
}