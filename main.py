#!/usr/bin/env python

import os
import socket
import sys

from physics import KineticMazeMotor

import odrive
from odrive.enums import *

TCP_IP = '127.0.0.1'
TCP_PORT = 7266
BUFFER_SIZE = 4

#Odrive setup
motor = KineticMazeMotor()


#Bind to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    data = s.recv(BUFFER_SIZE)

    #print ("Recieved type:", type(data), "\n")
    #print("Pre-parse raw:", data, "\n")

    angle = int.from_bytes(data, byteorder='little')

    #print("Post-proc type:", type(angle), "\n")
    #print("Post-proc raw:", angle, "\n")

    if angle != 0:
        motor.set_velocity(motor.adjust_angle(math.radians(angle)))
    else:
        motor.set_velocity(motor.ramp_down())

#Close socket if main loop broken
s.close()
