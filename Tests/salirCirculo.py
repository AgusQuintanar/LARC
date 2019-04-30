#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering
os.system('setfont Lat15-TerminusBold14')

#<---Puertos--->
#--Sensor Ultrasonico--
usIzq = UltrasonicSensor('in3') 
usIzq.mode='US-DIST-CM'
unitsIzq = usIzq.units                                                                                                            
distanceIzq = usIzq.value()  # convert mm to cm

#--Motores
MotIzq = LargeMotor('outB') #Motor Izquierdo
MotDer = LargeMotor('outA') #Motor derecho
MotBzo = LargeMotor('outC') #Motor de brazo

motoresTanquePair = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

def salirCirculo(distanceIzq):
    while distanceIzq != 255:
        print('Distancia',distanceIzq)
        error = 20-distanceIzq # Error = DistanciaReferencia - DistanciaReal
        vReal = 20
        k = .7
        wIzq = vReal + k*error
        wDer = vReal - k*error
        print('Izq:',wIzq,', Der:',wDer)
        motoresTanquePair.on(wIzq+25, wDer)
        distanceIzq = usIzq.value()
    motoresTanquePair.off(brake=True)
    motoresTanquePair.on_for_rotations(10, 10, .5)

def girar90GradosIzquierda():
    motoresTanquePair.on_for_degrees(-10, 10, 435, brake=True, block=True)

salirCirculo(distanceIzq)
girar90GradosIzquierda()