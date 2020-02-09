# -*- coding: utf-8 -*-
# plays Nessun Dorma on Agilent E4980A Precision LCR Meter

import visa
import traceback

a4=440.
b4=493.88
c5=554.365#523.25
d5=587.33
e5=659.255
f5=739.989#698.456
g5=783.991
a5=880.
b5=987.767

musicList = [[d5,8],
             [e5,8],
             [f5,8],
             [e5,8],
             [d5,8],
             [e5,6],
             [c5,16],
             [b4,1.6],#
             [e5,8],
             [f5,8],
             [g5,8],
             [f5,8],
             [e5,8],
             [f5,6],
             [d5,16],
             [c5,4],
             [d5,4],
             [e5,8],
             [e5,8],
             [f5,8],
             [g5,8],
             [a5,4],
             [a5,4],
             [a5,8],
             [a5,8],
             [a5,6],
             [f5,16],
             [f5,4],
             [f5,4],
             [f5,8],
             [f5,8],
             [f5,6],
             [d5,16],
             [a4,4],
             [a4,8],
             [a4,8],
             [a4,8],
             [a4,8],
             [e5,6],
             [c5,16],
             [d5,3],
             [b4,6],
             [d5,16],
             [g5,3],
             [d5,4],
             [b5,2.52],
             [a5,16],
             [a5,1]]
bpm = 77/1.1

def listToSound(l):
    freq = l[0]
    length = 60./bpm*4./l[1]
    return freq, length

def main():
    # open instrument
    rm = visa.ResourceManager("C:/Windows/System32/visa64.dll")
    pia = rm.open_resource('USB0::0x0957::0x8E18::MY51140120::0::INSTR')

    pia.write(":SYST:BEEP:STAT ON") # enable beep

    for l in musicList:
        freq, leng = listToSound(l)
        pia.write(f":SYST:BEEP {freq},{leng}")

main()
