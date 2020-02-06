import os
import errno

FIFO = '/tmp/fifo'


print("Opening FIFO...")
with open(FIFO) as fifo:
    print("FIFO opened")
    while True:
        data = fifo.read()
        if len(data) == 0:
            print("Writer closed")
        print('Read: "{0}"'.format(data))
