# To be used for speakers with the RPiMIB
# Written by Hannah Kleidermacher & Francis Pan
# May 2018

from time import sleep

freq_clock = 16000000 #Hz

class Amp():
        # NO JUMPERS = 3
        # LEFT SOLDERED = 2
        # RIGHT SOLDERED = 1
        # pls DON'T solder both pls
        def __init__(self, ad):
                self.address = ad | 0x48

        def setVolume(self, vol):
                # VOLUME 0-36
                self.volume = vol
                RPiMIB.sendI2C(self.address, vol)

class FG():
        # CHIP SELECT 1
        # CHIP SELECT 2
        # CHIP SELECT 3
        def __init__(self, chip):
                self.chipSelect = 0x10 << chip
                self.MSB = 0
                self.LSB = 0
                self.phase = 0

        def openData(self, port):
                sendFreq(0x2100, port)

        def closeData(self, port):
                sendFreq(0x2000, port)

        def sendData(self, input):
                data1 = input >> 8
                data2 = input & 0xFF

                RPiMIB.sendSPI(self.address, data1, data2) # command to write the next data to Function Generator 1

                print(input)

        def sendFreq(self, freq):
                global freq_clock
                #0x10000000 = 2^28
                #calculation for the frequency: converts wanted frequency to a 28-bit number, then scales by clock frequency
                freq_word=int(round(float(freq * 0x10000000) / freq_clock))
                #frequency word divide to two parts as MSB and LSB.
                # FFFC ->1111 1111 1111 1100 0000 0000
                self.MSB = (freq_word & 0xFFFC000) >> 14
                # 3FFF ->0011 1111 1111 1111
                self.LSB = (freq_word & 0x3FFF)
                #DB15 and DB14 are set to 0 and 1
                self.LSB |= 0x4000
                #DB15 and DB14 are set to 0 and 1
                self.MSB |= 0x4000
                #DB15, DB14,DB13 = 110 DB12 = x
                #respectively, which is the address for Phase Register 0.
                #The remaining 12 bits are the data bits and are all 0s in this case
                self.phase |= 0xC000

                openData()
                sendData(self.MSB)
                sendData(self.LSB)
                sendData(self.phase)
                closeData()

def playSound(fg, amp, freq, volume, duration):
        amp.setVolume(port, volume)
        fg.sendFreq(freq)
        sleep(duration)

def playSound(fg, amp, freq, volume):
        amp.setVolume(port, volume)
        fg.sendFreq(freq)
