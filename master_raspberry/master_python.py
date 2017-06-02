# Script must be run as root !!!
import smbus
import random, subprocess, time, os


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


def changeBaudrate(br=50000):
    global bus
    bus = ""
    run_command("sudo modprobe -r i2c_bcm2708")
    run_command("sudo modprobe i2c_bcm2708 baudrate="+str(br))
    bus = smbus.SMBus(1)
    
    #subprocess.check_output(["sudo", "modprobe", "-r", "i2c_bcm2708"])
    #subprocess.check_output(["sudo", "modprobe", "i2c_bcm2708", "baudrate="+str(br)])
    return 0


# Current baudrate
def getBaudrate():
    return run_command("sudo cat /sys/module/i2c_bcm2708/parameters/baudrate")


def writeNumber(value):
    bus.write_byte(slaves[0], value)
    # bus.write_byte_data(address, 0, value)
    return -1


def readNumber():
    number = bus.read_byte(slaves[0])
    # number = bus.read_byte_data(address, 1)
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

    #data_reliability *= 10
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

# i2c bus
bus = smbus.SMBus(1)

# Slave address
slaves = list()
slaves.append(0x08)

# vars
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