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

usDer = UltrasonicSensor('in4') 
usDer.mode='US-DIST-CM'
unitsDer = usDer.units                                                                                                            
distanceDer = usDer.value()  # convert mm to cm

#--Motores
MotIzq = LargeMotor('outB') #Motor Izquierdo
MotDer = LargeMotor('outA') #Motor derecho
MotBzo = LargeMotor('outC') #Motor de brazo

motoresTanquePair = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

def girar90GradosIzquierda():
    motoresTanquePair.on_for_degrees(-40, 40, 430, brake=True, block=True)

def girar90GradosDerecha():
    motoresTanquePair.on_for_degrees(40, -40, 430, brake=True, block=True)

def levantarBrazo():
    MotBzo.on_for_rotations(-25, .4)

def bajarBrazo():
    MotBzo.on_for_rotations(30, .38)
    MotBzo.run_to_rel_pos( stop_action="hold")

def salirFuerza():
    girar90GradosDerecha()
    motoresTanquePair.off(brake=True)
    motoresTanquePair.on_for_rotations(-50, -50, 6)
    motoresTanquePair.on_for_rotations(50, 50, .75)
    motoresTanquePair.off(brake=True)
    girar90GradosIzquierda()
    motoresTanquePair.off(brake=True)
    motoresTanquePair.on_for_rotations(-50, -50, 5)
    motoresTanquePair.on_for_rotations(50, 50, .4)
    motoresTanquePair.off(brake=True)
    girar90GradosDerecha()
    motoresTanquePair.off(brake=True)
    distanceDer = usDer.value() 
    while distanceDer < 200:
        motoresTanquePair.on(50,50)
        distanceDer = usDer.value()  
    motoresTanquePair.off(brake=True)
    motoresTanquePair.off(brake=True)
    motoresTanquePair.on_for_rotations(50, 10, .45)
    motoresTanquePair.off(brake=True)
    girar90GradosDerecha()


def dejarMonos():
    motoresTanquePair.on_for_rotations(30, 30, 7)
    motoresTanquePair.off(brake=True)
    levantarBrazo()
    motoresTanquePair.on_for_rotations(-30, -30, 2)
    motoresTanquePair.off(brake=True)
    bajarBrazo()
    salirFuerza()
    motoresTanquePair.on_for_rotations(100, 100, 3)


dejarMonos()