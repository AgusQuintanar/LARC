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


#<--Parámetros-->

colores = {"negro": [(28, 37, 14), 0], "blanco": [(310, 318, 158), 0], "rojo": [(195, 44, 17), 0], "azul": [(314, 169, 28), 0], "verde": [(42, 61, 17), 0], "afuera": [(11, 11, 6), 0]}
afueral = (17, 18, 11)
blancol = (245,275,157)
#--Sensor Ultrasonico--
usIzq = UltrasonicSensor('in3')
usIzq.mode = 'US-DIST-CM'
unitsIzq = usIzq.units
distanceIzq = usIzq.value()  # convert mm to cm

usDer = UltrasonicSensor('in4')
usDer.mode = 'US-DIST-CM'
unitsDer = usDer.units
distanceDer = usDer.value()  # convert mm to cm

#--Motores--
MotIzq = LargeMotor('outB') #Motor Izquierdo
MotDer = LargeMotor('outA') #Motor derecho
MotBzo = LargeMotor('outD') #Motor de brazo
motoresTanqueGirar = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')  
colSenDer.mode='RGB-RAW'
colSenIzq.mode='RGB-RAW'

def levantarBrazo():
    MotBzo.on_for_rotations(-30, .4)
    MotBzo.stop(stop_action="hold")

def bajarBrazo():
    MotBzo.on_for_rotations(30, .5)
    MotBzo.stop(stop_action="hold")

def girar90GradosDerecha():
    motoresTanqueGirar.on_for_degrees(15, -15, 432, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 432, brake=True, block=True)

def avanzarpor5cm():
    motoresTanqueGirar.on_for_seconds(15, 15, 1.6, brake=True, block=True)

def obtenerColorDer():
    valor = 25
    for col in colores:
        if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
            return col
    return 'afuera'
def obtenerColorIzq():
    if (abs(sum(blancol) - sum([colSenIzq.value(0), colSenIzq.value(1), colSenIzq.value(2)])) < 15):
        return 'blanco'
    return 'otro'


def salirFuerza():
    girar90GradosIzquierda()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 5)
    motoresTanqueGirar.on_for_rotations(50, 50, .4)
    motoresTanqueGirar.off(brake=True)
    girar90GradosDerecha()
    motoresTanqueGirar.off(brake=True)
    distanceDer = usDer.value()
    while distanceDer < 200:
        motoresTanqueGirar.on(25, 25)
        distanceDer = usDer.value()
    motoresTanqueGirar.on_for_rotations(30, 30, .69)
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_degrees(15, -15, 443, brake=True, block=True)
    
    colorDer = obtenerColorDer()
    colorIzq = obtenerColorIzq()
    
    salio = False
    atorado = False
    while not salio  and not atorado:
        colorDer = obtenerColorDer()
        colorIzq = obtenerColorIzq()
        avanzarpor5cm()
        if colorDer == 'blanco' and colorIzq != 'blanco':
            motoresTanqueGirar.on_for_rotations(-10, -30, .6)
        elif colorDer != 'blanco' and colorIzq == 'blanco':
            motoresTanqueGirar.on_for_rotations(-30, -10, .6)
        elif colorDer == 'blanco' and colorIzq == 'blanco':
            motoresTanqueGirar.on_for_rotations(-30, -30, 1)
            girar90GradosIzquierda()
            motoresTanqueGirar.off(brake=True)
            motoresTanqueGirar.on_for_rotations(-50, -50, 5)
            motoresTanqueGirar.on_for_rotations(50, 50, .4)
            motoresTanqueGirar.off(brake=True)
            atorado = True
            return False
        else:
            salio = True
            return True


def dejarMonos():
    color = obtenerColorDer()
    while color != 'negro':
        motoresTanqueGirar.on(50,50)
        color = obtenerColorDer()
    motoresTanqueGirar.on_for_rotations(30, 30, 1.5)
    motoresTanqueGirar.off(brake=True)
    levantarBrazo()
    motoresTanqueGirar.on_for_rotations(-30, -30, 1.7)
    motoresTanqueGirar.off(brake=True)
    bajarBrazo()
    girar90GradosDerecha()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 6)
    motoresTanqueGirar.on_for_rotations(50, 50, .75)
    motoresTanqueGirar.off(brake=True)
    salioCorrectamente = False
    while salioCorrectamente == False:
        salioCorrectamente = salirFuerza()
    avanzarpor5cm()


