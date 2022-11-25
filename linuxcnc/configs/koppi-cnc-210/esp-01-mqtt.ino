#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######
// ######## EXPERIMENTAL / DON'T USE IN PRODUCTION ######

const char *ssid =	"HITRON-XXXX";  // cannot be longer than 32 characters!
const char *pass =	"HE5YVXXXXXX";

// Update these with values suitable for your network.
IPAddress server(192, 168, 0, 3);

PubSubClient client(server);

void callback(const MQTT::Publish& pub) {
//  Serial.write(pub.payload(), pub.payload_len());
  if (pub.topic() == "esp-01/gp0") {
    if (pub.payload_len() == 1 && pub.payload()[0] == '0') {
      digitalWrite(0, LOW);
    } else if (pub.payload_len() == 1 && pub.payload()[0] == '1') {
      digitalWrite(0, HIGH);
    }
  } else if (pub.topic() == "esp-01/gp2") {
    if (pub.payload_len() == 1 && pub.payload()[0] == '0') {
      digitalWrite(0, LOW);
    } else if (pub.payload_len() == 1 && pub.payload()[0] == '1') {
      digitalWrite(0, HIGH);
    }
  }
}

void setup()
{
  pinMode(0, OUTPUT);
  pinMode(2, OUTPUT);
  
  // Setup console
  Serial.begin(9600);
  delay(10);
  Serial.println();
  Serial.println();

  client.set_callback(callback);

  WiFi.begin(ssid, pass);

  int retries = 0;
  while ((WiFi.status() != WL_CONNECTED)) {
    retries++;
    delay(500);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi connected");
  }
  
  char buffer[10];
  sprintf(buffer, "esp-01-%d", ESP.getChipId());
  if (client.connect(buffer)) {
    client.publish("esp-01/status","connected");
    client.publish("esp-01/gp0", "0");
    client.publish("esp-01/gp2", "0");
    client.subscribe("esp-01/gp0");
    client.subscribe("esp-01/gp2");
  }
}

void loop()
{
  client.loop();
}
