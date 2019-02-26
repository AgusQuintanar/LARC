#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
from time import sleep
import os
os.system('setfont Lat15-TerminusBold14')

while True:
    MotIzq = LargeMotor('outB')
    MotDer = LargeMotor('outA')
    MotIzq.run_forever(speed_sp=900)
    MotDer.run_forever(speed_sp=900)


