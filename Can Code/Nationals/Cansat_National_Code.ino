#include <TinyGPS++.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h> 
#include <Arduino.h>
#include "wiring_private.h" 
#include <Arduino_LSM6DS3.h>

// Variables for Internal IMU 
float gyrox, gyroy, gyroz; 
float accelx, accely, accelz;

//Pin Select for GPS module
Uart gpsSerial (&sercom0, 5, 6, SERCOM_RX_PAD_1, UART_TX_PAD_0);
// Attach the interrupt handler to the SERCOM
void SERCOM_Handler()
{
  gpsSerial.IrqHandler();
}

Uart picoSerial (&sercom1, 13, 8, SERCOM_RX_PAD_1, UART_TX_PAD_2); 
// Attach the interrupt handler to the SERCOM
void SERCOM1_Handler()
{
  picoSerial.IrqHandler();
}

// Create a TinyGPS++ object 
TinyGPSPlus gps;
int GPSBaud = 9600;

#define BMP288_ADDRESS 0x76
Adafruit_BMP280 bmp; // I2C

#define MQ135pin 21
float sensorValue; //variable to store sensor value

void setup() {
  // Start the Arduino hardware serial port at 115200 baud 
  Serial.begin(115200);

  // Start the software serial port at the GPS's default baud 
  // Reassign pins 5 and 6 to SERCOM alt
  pinPeripheral(5, PIO_SERCOM_ALT);
  pinPeripheral(6, PIO_SERCOM_ALT);

  // Reassign pins 13 and 8 to SERCOM (not alt this time) 
  pinPeripheral(13, PIO_SERCOM);
  pinPeripheral(8, PIO_SERCOM);

  // Start my new hardware serial 
  picoSerial.begin(9600);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!"); 
    while (1);
  }

  // Start new hardware serial
  gpsSerial.begin(GPSBaud);
  delay(100);
  // Update GPS baud rate to
  changeBaudrate();
  // Restart GPS serial with new speed
  delay(100);
  gpsSerial.flush();
  gpsSerial.begin(115200);

  unsigned status;
  status = bmp.begin(BMP280_ADDRESS);


  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or try a different address!"));
    Serial.print("SensorID was: 0X"); 
    Serial.println(bmp.sensorID(),16);
    Serial.print("ID of 0xFF probably means a bad address, a BMP 180 or BMP 085\n"); 
    Serial.print("ID of 0x56-0x58 represents a BMP 280,\n");
    Serial.print("ID of 0x60 represents a BME 280.\n");
    Serial.print("ID of 0x61 represents a BME 680.\n");   
  }
    
  /* Default settings from datasheet. */

  bmp.setSampling (Adafruit_BMP280::MODE_NORMAL,        /* Operating Mode. */
                   Adafruit_BMP280::SAMPLING_X2,        /* Temp. oversampling */
                   Adafruit_BMP280::SAMPLING_X16,       /* Pressure oversampling */
                   Adafruit_BMP280::FILTER_X16,         /* Filtering. */
                   Adafruit_BMP280::STANDBY_MS_500);    /* standby time. */
}

void loop() {
  picoSerial.println("bmp280(" + String(bmp.readAltitude (1813.25)) + "," +bmp.readTemperature() + "," + bmp.readPressure()+ ")" ); 
  picoSerial.println("mq135(" + String(analogRead (MQ135pin)) + ")");
  
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope (gyrox, gyroy, gyroz);
    picoSerial.println("imugyro(" +String(gyrox)+ "," +gyroy+ "," +gyroz+ ")" );
  }

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration (accelx, accely, accelz); 
    picoSerial.println("imugyro(" +String(accelx)+ "," +accely+ "," +accelz+ ")" );
  }

  // This sketch displays information every time a new sentence is correctly encoded. 
  while (gpsSerial.available() > 0)
    if (gps.encode(gpsSerial.read()))
      if (gps.location.isValid())
      {
      picoSerial.println("gpslocation(" + String((gps.location.lat(), 6)) + "," + (gps.location.lng(), 6) + "," + (gps.altitude.meters()) + ")" );
      }
      if (gps.date.isValid())
      {
      picoSerial.println("gpsdate("+String(gps.date.month())+","+gps.date.day()+","+gps.date.year() + ")");
      }
      if (gps.time.isValid())
      {
      picoSerial.println("gpstime("+String(gps.time.hour())+","+gps.time.minute()+","+gps.time.second()+","+gps.time.centisecond()+")" );
      }

}

void changeBaudrate() {
  // CFG-PRT
  byte packet[] = {
    0x85, // sync char 1 
    0x62, // sync char 2 
    0x06, // class
    0x00, // id
    0x14, // length  
    0x00, //
    0x01, // payload 
    0x00, // payload 
    0x00, // payload 
    0x00, // payload 
    0xD0, // payload
    0x08, // payload
    0x00, // payload
    0x00, // payload
    0x00, // payload
    0xC2, // payload
    0x01, // payload
    0x00, // payload
    0x07, // payload
    0x00, // payload
    0x03, // payload
    0x00, // payload
    0x00, // payload
    0x00, // payload
    0x00, // payload
    0x00, // payload

    0xC0, // CK_A
    0x7E, // CK_B
  };

  sendPacket(packet, sizeof(packet));
}
  
void sendPacket(byte *packet, byte len) { 
  for (byte i = 0; i < len; i++)
  {
    gpsSerial.write(packet[i]);
  }
} 