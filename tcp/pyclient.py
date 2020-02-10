#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 7266
BUFFER_SIZE = 80


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:
    data = s.recv(BUFFER_SIZE)

    print ("Init type:", type(data), "\n")
    print("Pre-parse:", data, "\n")

    pardata = int.from_bytes(data, byteorder='little')

    print("Post-parse type:", type(pardata), "\n")
    print("Post-parse:", pardata, "\n")

s.close()
