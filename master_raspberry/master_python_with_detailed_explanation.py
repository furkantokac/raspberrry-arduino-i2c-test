# Script must be run as root !!!

import smbus # module for i2c connection
import random, subprocess, time, os


# This function basically run command on the terminal. We need this 
# command to change the i2c baudrate because module doesn't contain
# this feature. Actually, i2c module also doing all the i2c operations
# by running the command on terminal because it is a low-level data
# protocol. Basically operation system handles this communication so
# its performance changes from OS to OS. I checked Raspian OS's i2c
# performance by this project. Actually its Linux kernel has direct 
# effect on the performance because i2c runs as driver on the system.
def run_command(command):
    command = command.rstrip()
    # Run the command and get output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        if len(output) == 0:
            output = "\0"
    except:
        print "[!] Run command error."
        output = False
    return output

# Baudrate change is done in this function
def changeBaudrate(br=50000):
    # This following 2 lines are very important. When we are entering this function,
    # we have active i2c connection on the memory, on the operation system. If we 
    # try to change its baudrate while its active, the Raspian OS doens't allow us to
    # do that. When we run the following 2 lines, Python destroy the i2c connection
    # on the memory so Raspian OS will let us to change the baudrate
    global bus
    bus = ""
    
    # modprobe is a program that adds, removes modules from the Linux kernel. As I 
    # said i2c is running on system level, we are using it to control our i2c driver
    # which is i2c_bcm2708. By the following command, we remove the i2c_bcm2708 on the
    # actively running kernel driver list. 
    run_command("sudo modprobe -r i2c_bcm2708")

    # and command to change the baudrate of i2c
    run_command("sudo modprobe i2c_bcm2708 baudrate="+str(br))

    # create the SMBus again. you can see what it does by module's source code. Just
    # locate the def open(self, bus) line
    # https://github.com/bivab/smbus-cffi/blob/master/smbus/smbus.py
    bus = smbus.SMBus(1)
    
    return 0


# Get the current baudrate
def getBaudrate():
    return run_command("sudo cat /sys/module/i2c_bcm2708/parameters/baudrate")


# Send "value" to corresponding slave. Default slave_id is "0"
def writeNumber(value, slave_id=0):
    bus.write_byte(slaves[slave_id], value)
    return -1


# Request data from the slave_id. Default slave_id is "0"
def readNumber(slave_id=0):
    number = bus.read_byte(slaves[slave_id])
    return number


def dataBomb():
    print "[+] Measuring the speed..."
    counter = 0
    try:
        while 1:
            writeNumber(1)
            counter += 1
    except:
        pass
    
    time.sleep(0.5)
    readNumber()
    print "Data limit :", counter
    return counter    


# if data is more than 1 byte, it sends it in pieces
def isDataSent(size, data=1):
    try:
        for _ in range(size):
            writeNumber(data)
    except:
        return 0 # means error
    
    readNumber()
    return 1 # means no error


def measureSpeed(debug=0):
    print "[+] Measuring the speed..."
    num_of_data=500
    while True:
        if debug:
            print "[+] Testing : ", num_of_data, "data"
            print "[+] Arduino should show", num_of_data*3, "as total."
            print "[+] --------------------"
            print ""
        
        if not isDataSent(num_of_data):
            num_of_data -= 500
            print "[!] Limit of data :", num_of_data
            return num_of_data
        
        num_of_data+=500
        time.sleep(0.5)


# data_reliablity is percentage, data_length is byte
def measureSpeedBaudrate(debug=0, data_reliability=10, data_length=128, first_baudrate=10000, baudrate_step=10000):
    print "-----------------------------------------"
    print "[-] Data Length      :", data_length, "byte"
    print "[-] Data Reliability : " + str(data_reliability)+"%"
    print "[-] First Baudrate   :", first_baudrate
    print "[-] Baudrate Step    :", baudrate_step
    print "-----------------------------------------"
    baudrate = first_baudrate
    flag_reliability = False


    while 1:
        if debug: print "[+] Testing :", baudrate,"baudrate"
        changeBaudrate(baudrate)
        
        for i in range(data_reliability):
            if not isDataSent(data_length):
                flag_reliability = True
                break
            time.sleep(0.01)
        
        if flag_reliability:
            if debug: print "[!] FAILED!"
            break
        
        baudrate += baudrate_step
        
        if debug: print "[+] Passed!"
        if debug: print ""
        time.sleep(0.1)

    baudrate -= baudrate_step
    return baudrate

# create i2c bus
bus = smbus.SMBus(1)

# Slave addresses
slaves = list()
slaves.append(0x08)

# dl: dataLenght, dr:dataReliability
dl = 16
dr = 100

for i in range(4):
    dl = 16
    for j in range(6):
        safe_baudrate = measureSpeedBaudrate(debug=0, data_reliability=dr, data_length=dl)
        print "Safe baudrate for the device :", safe_baudrate
        print ""
        dl *= 2
    dr += 25