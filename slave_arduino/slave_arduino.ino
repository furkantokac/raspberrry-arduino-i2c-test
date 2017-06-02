#include <Wire.h>

// Arduino's identity on i2c bus
#define SLAVE_ADDRESS 0x08

// Number that will receive from Raspberry. Normally, 
long unsigned int number = 0;
long unsigned int state = 0;
long unsigned int counter = 0;
 
void setup()
{
    pinMode(13, OUTPUT);
    Serial.begin(9600); // start serial for output
    
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);
    
    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");
}
 
void loop()
{
    delay(1000);
}
 
// callback for received data
void receiveData(int byteCount)
{ 
    while (Wire.available())
    {
        number = Wire.read();
        counter += number;
        //Serial.print("data received: ");
        //Serial.println(number);
        
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
 
// means data transfer is finished
void sendData()
{
    Serial.print("Received : ");
    Serial.print(counter);
    Serial.println(" byte");
    Wire.write(0);
    counter = 0;
}
