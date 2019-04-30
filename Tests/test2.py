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

colores = {"negro": [(31, 36, 15), 0], "blanco": [(310, 315, 157), 0], "rojo": [(208, 43, 18), 0], "azul": [(335, 172, 28), 0], "verde": [(38, 92, 25), 0], "afuera": [(23, 20, 11), 0]}
negro = (28, 35, 15)
afueral = (17, 18, 11)
afuera = (23, 20, 11)
blanco = (310, 315, 157)
blancol = (248, 261, 146)
rojo = (253, 45, 17)
azul = (306, 225, 33)
azulrampa = (0, 0, 0)
verde = (35, 95, 26)
run1 = True
run2 = False
run3 = False
run4 = False
sumazulrampa = azulrampa[0] + azulrampa[1] + azulrampa[2]
sumverde = verde[0]+verde[1]+verde[2]
sumafuera = afuera[0]+afuera[1]+afuera[2]
sumblanco = blanco[0]+blanco[1]+blanco[2]
sumblancol = blancol[0]+blancol[1]+blancol[2]
sumrojo = rojo[0]+rojo[1]+rojo[2]
sumazul = azul[0]+azul[1]+azul[2]
sumnegro = negro[0]+negro[1]+negro[2]
sumafueral = afueral[0]+afueral[1]+afueral[2]
direcciones = [2,2,2]
intento = 0
identificaciones = 0
color = "ninguno"
distinguir ="ninguno"
mayor = 3
valor = 100
rampa1 = "hola"
rampa2 = "kiubo"
monos = 0
cargamento = False
juego = True
rango = 30


#<---Puertos--->

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
MotBzo = LargeMotor('outC') #Motor de brazo
motoresTanqueGirar = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')  
colSenDer.mode='RGB-RAW'
colSenIzq.mode='RGB-RAW'


def salirFuerza():
    girar90GradosDerecha()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 6)
    motoresTanqueGirar.on_for_rotations(50, 50, .75)
    motoresTanqueGirar.off(brake=True)
    girar90GradosIzquierda()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 5)
    motoresTanqueGirar.on_for_rotations(50, 50, .4)
    motoresTanqueGirar.off(brake=True)
    girar90GradosDerecha()
    motoresTanqueGirar.off(brake=True)
    distanceDer = usDer.value()
    while distanceDer < 200:
        motoresTanqueGirar.on(50, 50)
        distanceDer = usDer.value()
    motoresTanqueGirar.on_for_rotations(30, 30, .4)
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(50, 10, 0.35)
    motoresTanqueGirar.off(brake=True)
    girar90GradosDerecha()


def dejarMonos():
    motoresTanqueGirar.on_for_rotations(30, 30, 4.5)
    motoresTanqueGirar.off(brake=True)
    levantarBrazo()
    motoresTanqueGirar.on_for_rotations(-30, -30, 2)
    motoresTanqueGirar.off(brake=True)
    bajarBrazo()
    salirFuerza()
 


def levantarBrazo():
    MotBzo.on_for_rotations(-50, .4)
    MotBzo.stop(stop_action="hold")

def bajarBrazo():
    MotBzo.on_for_rotations(50, .5)
    MotBzo.stop(stop_action="hold")

def girar90GradosDerecha():
    motoresTanqueGirar.on_for_degrees(15, -15, 437, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 437, brake=True, block=True)

def alinearseiniciocuidado():
    continuar = "no"
    avanzarpor5cmreversa()
    while continuar == "no":
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 50)):
            avanzarporsiemprecuidadoextremo()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 50)):
            avanzarporsiempreizquierdacuiado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 50)):
            avanzarporsiemprederechacuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 50)):
            continuar = "si"
#<--Promaga-->
    for col in colores:
        if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
            valor = abs(sum(
                colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
            distinguir = col
    valor = 100
