# Raspberry Arduino I2C Test
---------------
# Master
- Raspberry Pi 3 Version B
- I2C installation and necessary settings are told in the report.
- Uses Python2.7
- Raspian Information
	PRETTY_NAME="Raspbian GNU/Linux 8 (jessie)"
	NAME="Raspbian GNU/Linux"
	VERSION_ID="8"
	VERSION="8 (jessie)"
	ID=raspbian
- More slaves can be added easily by adding its address to the code
	If new slave's address is 0x09, add the command to the line 134
	slaves.append(0x09)
- Currently, when the code is run, it directly start testing the baudrate by starting from 10000bit per second and it keeps going by adding 10000 like 10000bit, 20000bit, 30000bit etc. It stops when the baudrate is fail.


# Slave
- Arduino Uno V3
- Arduino IDE 1.6.11
- It can be directly installed to Arduino
- The process can be monitored from "Serial Monitor" on Ardunio IDE. (Port 9600)
- To watch the incoming data, a LED can be put to pin 13 so it will flash each time data received.
