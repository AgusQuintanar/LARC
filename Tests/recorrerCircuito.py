#!/usr/bin/env python3
#So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering
os.system('setfont Lat15-TerminusBold14')

#<---Puertos--->
#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')  
colSenDer.mode='RGB-RAW'
colSenIzq.mode='RGB-RAW'

#--Motores
MotIzq = LargeMotor('outB') #Motor Izquierdo
MotDer = LargeMotor('outA') #Motor derecho
#MotBzo = LargeMotor('outC') #Motor de brazo

motoresTanquePair = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

       
colores = { "negro":[(30,40,14),0], "blanco":[(308,319,153),0], "rojo":[(263,52,16),0], "azul":[(319,235,32),0], 
			"verde":[(35, 93, 24),0], "afuera":[(20,19,11),0]}
def girar90GradosDerecha():
    motoresTanquePair.on_for_degrees(10, -10, 435, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanquePair.on_for_degrees(-10, 10, 435, brake=True, block=True)

def identificarColor():
    for col in colores:
        if abs(sum([colores[col][0][x] - colSenDer.value(x) for in range(3)])) < 15:
            return col
	return 'ninguno'


def llegarAColor(): 
    color = identificarColor()
    while color=='blanco':
        motoresTanquePair.on(40,40)
    


while True:
    print(identificarColor())
    print([colSenDer.value(0),colSenDer.value(1),colSenDer.value(2)])
