#include <Wire.h>

// Arudino's identity
#define SLAVE_ADDRESS 0x08

// Number that will be received from Raspberry.
// Normally this number is 1 byte but I also tested
// different numbers and I saw that it is not stable
// and universal.
long unsigned int number = 0;

// When Arduino receive data, it light on the led that
// is located at port 13. When it receive data again,
// it light off that led. This variable keep the state
// of the led.
long unsigned int state = 0;

// Count the number of byte received. Counter 8 means
// 8 byte data received because each time Master sends
// 1 byte data
long unsigned int counter = 0;
 
void setup()
{
	// pin 13 is output for led
    pinMode(13, OUTPUT);
    
    // start serial port 9600 for debugging
    Serial.begin(9600);
    
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS); 
    
    // define callbacks for i2c communication.
    // Run "receiveData" function when receive data
    Wire.onReceive(receiveData);
    // Run "onRequest" function when Master request data
    Wire.onRequest(sendData);

    Serial.println("Ready!");
}
 
void loop()
{
	// i2c using interrupt so nothing to do with this delay
    delay(1000);
}
 
// callback for received data
void receiveData(int byteCount)
{
	// In I2C protocol, Master firstly send a signal and make the
	// slave available, start the communication. After data send 
	// finished, Master send a signal and close the connection.
    while (Wire.available())
    {
    	// Read the data
        number = Wire.read();
        counter += number;

        // Optionally, you can debug the received data
        //Serial.print("data received: ");
        //Serial.println(number);
        
        // Arrange the led.
        if (state == 0)
        {
            digitalWrite(13, HIGH); // set the LED on
            state = 1;
        } else
        {
            digitalWrite(13, LOW); // set the LED off
            state = 0;
        }
    }
}
 
// callback for request data
// for my code, when data transfer is finished,
// Master will run this function
void sendData()
{
    Serial.print("Received : ");
    Serial.print(counter);
    Serial.println(" byte");

    // Send "0" integer to Master
    Wire.write(0);
    
    counter = 0;
}
