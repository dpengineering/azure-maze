import os

kmm = None

while True:

    with open('./tracking-module/anglelog.txt') as  f:
        hist = list(f)
        #Have way to remove history after writing? in C
