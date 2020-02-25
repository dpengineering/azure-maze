# To be used for the RPiMIB designed for the DPEA by Joe Kleeberg
# Compiled by Hannah Kleidermacher, Francis Pan, and Doug Whetter
# May 2018


import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from threading import Thread

SHUTDOWN_PORT = 21
CLOCK_POLARITY_MODE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(SHUTDOWN_PORT, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# set up SPI between the Raspberry Pi and the PiMIB board
spi = spidev.SpiDev()
#spiFrequency = 16000000
spiFrequency = 1000000

#takes 0, 1, or 2
def readEncoder(encoder):

    print("Read Encoder: ")

    spi.xfer([0x00, 0x10], spiFrequency, 1)                      # sending this command tells PiMIB to send back encoder data
    enc0_list_of_bytes = spi.xfer([0x00, 0x00], spiFrequency, 1)  # getting data for encoder A
    enc1_list_of_bytes = spi.xfer([0x00, 0x00], spiFrequency, 1)
    enc2_list_of_bytes = spi.xfer([0x00, 0x00], spiFrequency, 1)
    enc0 = 0x100*enc0_list_of_bytes[0] + enc0_list_of_bytes[1]  # convert the two bytes received into encoder value
    enc1 = 0x100*enc1_list_of_bytes[0] + enc1_list_of_bytes[1]
    enc2 = 0x100*enc2_list_of_bytes[0] + enc2_list_of_bytes[1]

    if encoder == 0:
        if (enc0 & 0xf000) :         # encoder has 12-bit value  PiMIB sends back xF000 if encoder not pulgged in
            print("Encoder A not plugged in")
        return enc0

    if encoder == 1:
        if (enc1 & 0xf000) :
            print("Encoder B not plugged in")
        return enc1

    if encoder == 2:
        if (enc2 & 0xf000) :
            print("Encoder C not plugged in")
        return enc2

def openSPI():
    print("openSPI")
    spi.open(0,0)
    spi.mode = CLOCK_POLARITY_MODE

def closeSPI():
    print("closeSPI");
    spi.close()

def reset():
    print("Reset");
    #spi.xfer([0xff, 0xff], spiFrequency, 1);
    #sleep(5)

def sendSPI(address, data1, data2):
    print("Send SPI: " + str(data1) + " address: " + str(address))
    spi.xfer([0x00, address], spiFrequency, 1)  # command to write the next data to Function Generator 1
    spi.xfer([data1, data2], spiFrequency, 1)  #  data 0x1234 sent to function generator 1 using the SPI connector 1

def sendI2C(address, data):
    spi.xfer([0x00, 0x80], spiFrequency, 1)  #command to write following data over I2C on connector 1
    spi.xfer([address, data], spiFrequency, 1)  # I2C write to IC address 0x41 with data 0x17  0x41 = Amp1
    print("Send I2C: " + str(hex(address)) + " address: " + str(hex(data)))

def sendPWM(pin, data):
    MsByte = data >> 8
    LsByte = data & 0x00ff

    address = pin - 3
    spi.xfer([address, 0x00], spiFrequency, 1)  #command to write following data to pwm_a
    spi.xfer([MsByte, LsByte], spiFrequency, 1)
    print("Send PWM: data: " + str(data) + " address: " + str(hex(address)) + " M: " + str(hex(MsByte)) + " L: " + str(hex(LsByte)))

def cleanup():
    spi.close()
    GPIO.remove_event_detect(SHUTDOWN_PORT)
    GPIO.cleanup()

def shutdown():
    cleanup();
    print("Shutting down in 2 seconds")
    sleep(2)
    os.system("sudo shutdown now -h")

def shutdownHandler():
    print("Shutdown Handler Started");
    GPIO.wait_for_edge(SHUTDOWN_PORT, GPIO.FALLING)
    shutdown()

def startShutdownHandlerThread():
    t = Thread(target=shutdownHandler)
    t.start()
def setFrequency(freq):
    global spiFrequency
    spiFrequency = freq
