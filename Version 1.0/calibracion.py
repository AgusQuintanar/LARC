#!/usr/bin/env python3
#So program can be run from Brickman


#<--Importar librerías-->

from ev3dev.ev3 import *
from time import sleep
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering
os.system('setfont Lat15-TerminusBold14')

#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')
colSenDer.mode = 'RGB-RAW'
colSenIzq.mode = 'RGB-RAW'
x = "s"

while x=="s":
    print(colSenDer.value(0), ", ", colSenDer.value(1), ", ", colSenDer.value(2))
    print(colSenIzq.value(0), ", ", colSenIzq.value(1), ", ", colSenIzq.value(2))
    sleep(5)


