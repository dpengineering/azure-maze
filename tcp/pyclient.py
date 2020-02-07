#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 7266
BUFFER_SIZE = 80


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    s.connect((TCP_IP, TCP_PORT))
    data = s.recv(BUFFER_SIZE)
    s.close()

    print "Received data:", data
