#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
os.system('setfont Lat15-TerminusBold14')

#<---Puertos--->
#--Sensor Ultrasonico--
# us = UltrasonicSensor() 
# us.mode='US-DIST-CM'
# units = us.units                                                                                                            
# distance = us.value()/10  # convert mm to cm

#--Motores
MotIzq = LargeMotor('outB') #Motor Izquierdo
MotDer = LargeMotor('outA') #Motor derecho
MotBzo = LargeMotor('outC') #Motor de brazo

#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')  
colSenDer.mode='COL-COLOR'
colSenIzq.mode='COL-COLOR'
colors=('unknown','black','blue','green','yellow','red','white','brown')

def obtenerColor():
    return [colors[colSenDer.value()],colors[colSenIzq.value()]]
       
def noSalirse():
    if obtenerColor()[0] == 'unknown':
        MotIzq.stop(stop_action="hold")
        delay(.8)
        MotDer.on_for_seconds(speed=10, seconds=1)
    
        MotIzq.stop(stop_action="hold")

    elif obtenerColor()[1] == 'unknown':
        MotDer.on_for_seconds(speed=5, seconds=.3)
        sleep(1)
        MotIzq.on_for_seconds(speed=10, seconds=1)

def levantarBrazo():
    MotBzo.on_for_rotations(-50, .3)

def bajarBrazo():
    MotBzo.on_for_rotations(50, .28)


def stopRobotAtPerson(distance):
    while distance > 30:   
        print(str(distance) + " " + units)
        MotIzq.run_forever(speed_sp=800)
        MotDer.run_forever(speed_sp=800)
        #noSalirse()
        distance = us.value()/10  # convert mm to cm

    MotIzq.stop(stop_action="hold")
    MotDer.stop(stop_action="hold")

def recogerMono():
    levantarBrazo()
    MotIzq.run_forever(speed_sp=500)
    MotDer.run_forever(speed_sp=500)
    sleep(1)
    MotIzq.stop(stop_action="hold")
    MotDer.stop(stop_action="hold")
    bajarBrazo()
    MotIzq.run_forever(speed_sp=-500)
    MotDer.run_forever(speed_sp=-500)
    sleep(.1)

def girar90GradosDerecha():
    MotIzq.run_forever(speed_sp=-500)
    MotDer.run_forever(speed_sp=500)
    sleep(1.17)
    MotIzq.stop(stop_action="hold")
    MotDer.stop(stop_action="hold")


    



def main():
    recogerMono()


main()
