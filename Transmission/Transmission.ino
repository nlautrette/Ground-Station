#include <SoftwareSerial.h>

// Transmission related variables
unsigned long RXbaudRate = 57600; // UPDATE if changed
#define numSensors 10 // UPDATE if changed
#define valueChars 5 // UPDATE if changed
// For the total size of the sensorReadings
// 2 chars reserved for start and stop
#define transmissionPacketSize (numSensors * valueChars) + 2
bool readSensor[numSensors];
char sensorReadings[transmissionPacketSize]; 


// Sensor reading variables
SoftwareSerial sensorSerial;
unsigned long sensorBaudRate = 57600; // UPDATE if changed
#define startChar '('
#define endChar ')'
#define packetLength 7 // UPDATE if changed, excluding the start and endChars
#define keyLength 2 // UPDATE if changed
#define valueLength packetLength - keyLength
char packetKey[keyLength];
char packetValue[valueLength];

// Packet processing variables
bool started = false;
bool ended = false;
byte packetIndex = 0;

void setup() {
  // Setup serials
  Serial.begin(RXbaudRate); // Debug serial
  Serial1.begin(RXbaudRate); // Transceiver serial
  sensorSerial.begin(sensorBaudRate, 2, 3); // RS485 serial
}

void loop() {
  while(sensorSerial.available() > 0) {
    // Populate the char arrays for the key value pairs for the sensors
    char inChar = sensorSerial.read();
    if (inChar == startChar) {
      started = true;
    } else if (inChar == endChar) {
      ended = true;
      break;
    } else if (started) {
      if (packetIndex >= 0 && packetIndex < keyLength) {
        packetKey[packetIndex] = inChar;
      } else if (packetIndex >= keyLength && packetIndex < packetLength) {
        packetValue[packetIndex] = inChar;
      } else {
        //Invalid index
        break;
      }
      packetIndex++;
    }
  }

  if (started && ended && packetIndex == packetLength - 1) {
    // Process this packet of format index[0-1], value[2-11]
    int index = atoi(packetKey);
    int value = atoi(packetValue);
    sensorReadings[index] = value;
    // We've read this sensor's value so set it to true,
    // index - 1 because our sensor ids start at 1
    readSensor[index - 1] = true;
  } else {
    // The packet is not in the right format
    Serial.println("Bad packet received, skipped packet");
  }

  // Reset to process next packet
  started = false; ended = false; packetIndex = 0;


  // Setup packet for transmission
  String transmissionPacket = "(";
  
  // Check that all sensor readings have been received
  for (byte i = 0; i < numSensors; i++) {
    if (!readSensor[i]) {
      // Sensor has not been read, break
      break;
    }
    if (i == numSensors - 1) {
      // We've reached the last index and all have been true,
      // therefore we've received all the sensor readings,
      // send the sensor data;
      Serial1.print(sensorReadings);
      emptyArray(sensorReadings);
    }
  }
}

void emptyArray (char charArray[]) {
  for (int i = 0; i < sizeof(charArray); i++) {
    charArray[i] = '\0';
  }
}
