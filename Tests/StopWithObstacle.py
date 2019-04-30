#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
from time import sleep
import os
os.system('setfont Lat15-TerminusBold14')

us = UltrasonicSensor() 
us.mode='US-DIST-CM'
units = us.units                                                                                                            
distance = us.value()/10  # convert mm to cm
MotIzq = LargeMotor('outB')
MotDer = LargeMotor('outA')

while distance > 30:    # Stop program by pressing touch sensor button
    print(str(distance) + " " + units)
    MotIzq.run_forever(speed_sp=500)
    MotDer.run_forever(speed_sp=500)
    distance = us.value()/10  # convert mm to cm

MotIzq.stop(stop_action="hold")
MotDer.stop(stop_action="hold")

