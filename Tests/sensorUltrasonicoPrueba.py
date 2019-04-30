#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering
os.system('setfont Lat15-TerminusBold14')

#<---Puertos--->
#--Sensores Ultrasonicos--
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

#--Sensor de color--
colores = {"negro": [(30, 40, 14), 0], "blanco": [(308, 319, 153), 0], "rojo": [(263, 52, 16), 0], "azul": [(319, 235, 32), 0], "verde": [(35, 93, 24), 0], "afuera": [(20, 19, 11), 0]}


def obtenerColor():
    return 0
       
def noSalirse():
    return 0

def levantarBrazo():
    MotBzo.on_for_rotations(-25, .4)

def bajarBrazo():
    MotBzo.on_for_rotations(50, .6)
    MotBzo.stop(stop_action = "hold")

def stopRobotAtPerson(distanceIzq, distanceDer):
    while True:
        if distanceIzq <30 and distanceDer<30:
            return 0
        elif distanceIzq < 30:
            return -1
        elif distanceDer < 30:
            return 1
        motoresTanquePair.on(30,30)
        distanceIzq = usIzq.value()
        distanceDer = usDer.value()


def recogerMonoIzquierda():
    levantarBrazo()
    girar90GradosIzquierda()
    motoresTanquePair.on_for_rotations(10, 10, 1)
    bajarBrazo()
    motoresTanquePair.on_for_rotations(-10, -10, 1)
    girar90GradosDerecha()

def recogerMonoDerecha():
    levantarBrazo()
    girar90GradosDerecha()
    motoresTanquePair.on_for_rotations(10, 10, 1)
    bajarBrazo()
    motoresTanquePair.on_for_rotations(-10, -10, 1)
    girar90GradosIzquierda()

def recogerMono():
    direccion = stopRobotAtPerson(50,50)
    bandera = True
    
    motoresTanquePair.off(brake=True)
    if direccion == -1:
        recogerMonoIzquierda()
        motoresTanquePair.on_for_seconds(-10, -10, 2, brake=True, block=True)
    else:
        recogerMonoDerecha()
        motoresTanquePair.on_for_seconds(-10, -10, 2, brake=True, block=True)


def girar90GradosDerecha():
    motoresTanquePair.on_for_degrees(10, -10, 435, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanquePair.on_for_degrees(-10, 10, 435, brake=True, block=True)
    

def main():
    recogerMono()
    recogerMono()
   

main()
