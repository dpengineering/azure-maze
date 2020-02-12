#!/usr/bin/env python

import os
import socket
import sys
import math

from physics import KineticMazeMotor

import odrive
from odrive.enums import *

TCP_IP = '127.0.0.1'
TCP_PORT = 7266
BUFFER_SIZE = 4



#Bind to socket
print("[Py] Starting socket client...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("[Py] Socket connected!")

#Odrive setup, auto calibrate/initializes
motor = KineticMazeMotor()

print("Beginning control loop!\n")
while True:
    data = s.recv(BUFFER_SIZE)

    #print ("Recieved type:", type(data), "\n")
    #print("Pre-parse raw:", data, "\n")

    angle = int.from_bytes(data, byteorder='little', signed=True)

    #print("Post-proc type:", type(angle), "\n")
    print("Post-proc raw:", angle, "\n")

    if angle not in range(20,-20):
            motor.set_velocity(motor.adjust_angle(math.radians(-angle)))

    else:
            motor.set_velocity(motor.ramp_down())

#Close socket if main loop broken
s.close()
