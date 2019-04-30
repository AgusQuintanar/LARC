#!/usr/bin/env python3
#So program can be run from Brickman


#<--Importar librerías-->

from ev3dev.ev3 import *
from time import sleep, time
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering
os.system('setfont Lat15-TerminusBold14')


#<--Parámetros-->

colores = {"negro": [(23,23,28), 0], "blanco": [(256, 281, 250), 0], "rojo": [(170,27,36), 0], "azul": [(270, 160, 52), 0], "verde": [(32, 50, 29), 0], "afuera": [(10,6,7), 0]}
blancol = (296, 310, 150)
negro = (23,23,28)
afueral = (9,7,3)
afuera = (10,6,7)
negro = (28, 35, 15)
blanco = (256, 281, 250)
rojo = (253, 45, 17)
azul = (306, 225, 33)
azulrampa = (0, 0, 0)
verde = (35, 95, 26)
run1 = True
run2 = False ##
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
cargamento = False ###
juego = True
rango = 22
rangoizq = 24
rango2 = 100
rango3 = 60
t1 = time()


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
MotBzo = LargeMotor('outD') #Motor de brazo
motoresTanqueGirar = MoveTank(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B,OUTPUT_A) #Concatena los 2 motores para usar funciones de tiempo

#--Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')  
colSenDer.mode='RGB-RAW'
colSenIzq.mode='RGB-RAW'


#<--Funciones-->

def salirFuerza():
    girar90GradosIzquierda()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 5)
    motoresTanqueGirar.on_for_rotations(50, 50, .7)
    motoresTanqueGirar.off(brake=True)
    girar90GradosDerecha()
    motoresTanqueGirar.off(brake=True)
    distanceDer = usDer.value()
    while distanceDer < 200:
        motoresTanqueGirar.on(25, 25)
        distanceDer = usDer.value()
    motoresTanqueGirar.on_for_rotations(30, 30, .69)
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_degrees(15, -15, 437, brake=True, block=True)
    
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

def levantarBrazo():
    MotBzo.on_for_rotations(-50, .4)
    MotBzo.stop(stop_action="hold")

def bajarBrazo():
    MotBzo.on_for_rotations(50, .5)
    MotBzo.stop(stop_action="hold")

def stopRobotAtPerson(distanceIzq, distanceDer):
    while True:
        if distanceIzq < 30 and distanceDer < 30:
            return 0
        elif distanceIzq < 30:
            return -1
        elif distanceDer < 30:
            return 1
        distanceIzq = usIzq.value()
        distanceDer = usDer.value()

def recogerMonoIzquierda():
    levantarBrazo()
    girar90GradosIzquierda()
    t1 = time()
    continuar = "si"
    while ((time()-t1) < 1.05) & (continuar == "si") :
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprecuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            avanzarporsiempreizquierda()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprederecha()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            continuar = "no"

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosDerecha()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosDerecha()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosDerecha()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
        motoresTanqueGirar.on_for_rotations(-10, -10, .4)
        bajarBrazo()
        girar90GradosDerecha()

    girar90GradosDerecha()
    continuar = "si"
    t1 = time()
    while (continuar == "si"):
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprecuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            avanzarporsiempreizquierda()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprederecha()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            continuar = "no"
    motoresTanqueGirar.on_for_rotations(-10, -10, .4)
    girar90GradosIzquierda()


def recogerMonoDerecha():
    levantarBrazo()
    girar90GradosDerecha()
    t1 = time()
    continuar = "si"
    while ((time()-t1) < 1.05) & (continuar == "si"):
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprecuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            avanzarporsiempreizquierda()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprederecha()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            continuar = "no"

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosIzquierda()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosIzquierda()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
        motoresTanqueGirar.on_for_rotations(10, 10, .45)
        bajarBrazo()
        motoresTanqueGirar.on_for_rotations(-10, -10, .85)
        girar90GradosIzquierda()

    if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
        motoresTanqueGirar.on_for_rotations(-10, -10, .4)
        bajarBrazo()
        girar90GradosIzquierda()
    
    girar90GradosIzquierda()
    continuar = "si"
    t1 = time()
    while (continuar == "si"):
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprecuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            avanzarporsiempreizquierda()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < rango3)):
            avanzarporsiemprederecha()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > rango3) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > rango3)):
            continuar = "no"
    motoresTanqueGirar.on_for_rotations(-10, -10, .35)
    girar90GradosDerecha()

def recogerMono():
    direccion = stopRobotAtPerson(distanceIzq, distanceDer)

    motoresTanqueGirar.off(brake=True)
    if direccion == -1:
        recogerMonoIzquierda()
        #motoresTanqueGirar.on_for_seconds(-10, -10, 2, brake=True, block=True)
    else:
        recogerMonoDerecha()
        #motoresTanqueGirar.on_for_seconds(-10, -10, 2, brake=True, block=True)

def girar90GradosDerecha():
    motoresTanqueGirar.on_for_degrees(15, -15, 432, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 432, brake=True, block=True)

def girarIzquierda():
    continuar = "no"
    avanzarpor5cm()
    while continuar == "no":
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 50)):
            avanzarporsiemprereversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 50)):
            avanzarporsiempreizquierdareversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 50)):
            avanzarporsiemprederechareversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 50) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 50)):
            avanzar3cmreversa()
            continuar = "si"
    girar90GradosIzquierda()

def avanzarporsiempre():
    motoresTanqueGirar.on(27, 27)

def avanzarporsiemprecuidado():
    motoresTanqueGirar.on(10, 10)

def avanzarporsiemprecuidadoextremo():
    motoresTanqueGirar.on(5, 5)

def avanzarporsiemprederecha():
    motoresTanqueGirar.on(10, 0)

def avanzarporsiempreizquierda():
    motoresTanqueGirar.on(0, 10)

def avanzarporsiemprederechacuidado():
    motoresTanqueGirar.on(5, 0)

def avanzarporsiempreizquierdacuiado():
    motoresTanqueGirar.on(0, 5)

def avanzarporsiemprederechareversa():
    motoresTanqueGirar.on(-10, 0)

def avanzarporsiempreizquierdareversa():
    motoresTanqueGirar.on(0, -10)

def avanzarporsiemprereversa():
    motoresTanqueGirar.on(-10, -10)

def avanzarpor15cmreversa():
    motoresTanqueGirar.on_for_seconds(-30, -30, 1.45, brake=True, block=True)

def avanzarpor15cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 1.45, brake=True, block=True)

def avanzarpor30cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 2, brake=True, block=True)

def avanzarpor1cm():
    avanzarporsiempre()
    #motoresTanqueGirar.on_for_seconds(30, 30, 0.5, brake=True, block=True)

def avanzarpor5cm():
    motoresTanqueGirar.on_for_seconds(15, 15, 1.8, brake=True, block=True)

def avanzarpor5cmreversa():
    motoresTanqueGirar.on_for_seconds(-15, -15, 1.8, brake=True, block=True)

def avanzar3cmreversa():
    motoresTanqueGirar.on_for_seconds(-15, -15, 0.6, brake=True, block=True)

def avanzar3cm():
    motoresTanqueGirar.on_for_seconds(15, 15, 0.75, brake=True, block=True)

def minigiroizq():
    motoresTanqueGirar.on_for_degrees(-15, 15, 50, brake=True, block=True)

def minigiroder():
    motoresTanqueGirar.on_for_degrees(15, -15, 50, brake=True, block=True)

def alinearse():
    continuar = "no"
    avanzarpor5cm()
    while continuar == "no":
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprereversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            avanzarporsiempreizquierdareversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprederechareversa()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            avanzarpor5cm()
            continuar = "si"

def alinearseinicio():
    continuar = "no"
    avanzarpor5cmreversa()
    while continuar == "no":
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprecuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            avanzarporsiempreizquierda()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprederecha()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            continuar = "si"

def alinearseiniciocuidado():
    continuar = "no"
    avanzarpor5cmreversa()
    while continuar == "no":
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprecuidadoextremo()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) < 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            avanzarporsiempreizquierdacuiado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) < 80)):
            avanzarporsiemprederechacuidado()
        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumblanco)) > 70) & ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumblancol)) > 80)):
            continuar = "si"


#<--Programa-->
while juego == True:
    while run1 == True:
    #asa

        for col in colores:
            if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                distinguir = col
        valor = 100

        if ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumafueral)) < 10):
            distinguir = "afueral"

        if (distinguir == "afueral"):
            avanzar3cmreversa()
            minigiroder()

        if (distinguir == "afuera"):
            avanzar3cmreversa()
            minigiroizq()

        if (distinguir == "blanco"):
            avanzarpor1cm()

        if (distinguir == "negro"):
            #color="negro"
            alinearseinicio()
            motoresTanqueGirar.on_for_rotations(-10, -10, .4)
            girar90GradosIzquierda()
            girar90GradosIzquierda()
            intento = intento + 1


        if (distinguir == "rojo"):
            
            if direcciones[0] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0]==2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[0] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[0] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[0] == 2:

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0
                    color = "rojo"
                    identificaciones = identificaciones + 1

                if intento == 4:
                    intento = intento +1

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0
                    color = "rojo"
                    identificaciones = identificaciones + 1

                if intento == 2:
                    intento = intento + 1

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0
                    color = "rojo"
                    identificaciones = identificaciones + 1

                if intento == 0:
                    intento = 1
                    color = "rojo"
                
                if direcciones[0] == -1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

                if direcciones[0] == 0:
                    alinearseinicio()
                    avanzarpor30cm()
                    alinearse()

                if direcciones[0] == 1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosDerecha()
                    alinearse()

                if direcciones[0] == 2:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

        if (distinguir == "verde"):
            
            if direcciones[1] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[1] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[1] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[1] == 2:

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0
                    color = "verde"
                    identificaciones = identificaciones + 1

                if intento == 4:
                    intento = 5

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0
                    color = "verde"
                    identificaciones = identificaciones + 1

                if intento == 2:
                    intento = 3

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0
                    color = "verde"
                    identificaciones = identificaciones + 1

                if intento == 0:
                    intento = 1
                    color = "verde"
                
                if direcciones[1] == -1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()
                
                if direcciones[1] == 0:
                    alinearseinicio()
                    avanzarpor30cm()
                    alinearse()
                
                if direcciones[1] == 1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosDerecha()
                    alinearse()
                
                if direcciones[1] == 2:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

        if (distinguir == "azul"):

            if direcciones[2] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[2] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[2] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0

            if direcciones[2] == 2:

                if intento == 5:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 1
                    intento = 0
                    color = "azul"
                    identificaciones = identificaciones + 1

                if intento == 4:
                    intento = 5

                if intento == 3:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = 0
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = 0
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = 0
                    intento = 0
                    color = "azul"
                    identificaciones = identificaciones + 1

                if intento == 2:
                    intento = 3

                if intento == 1:
                    if (color == "rojo") & (direcciones[0] == 2):
                        direcciones[0] = -1
                    if (color == "verde") & (direcciones[1] == 2):
                        direcciones[1] = -1
                    if (color == "azul") & (direcciones[2] == 2):
                        direcciones[2] = -1
                    intento = 0
                    color = "azul"
                    identificaciones = identificaciones + 1

                if intento == 0:
                    intento = 1
                    color = "azul"
                
                if direcciones[2] == -1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

                if direcciones[2] == 0:
                    alinearseinicio()
                    avanzarpor30cm()
                    alinearse()

                if direcciones[2] == 1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosDerecha()
                    alinearse()

                if direcciones[2] == 2:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

        if (direcciones[0] != 2) & (direcciones[1] != 2) & (direcciones[2] != 2) :
            run1 = False
            run2 = True

        print("color", color)
        print("intento", intento)
        print("direcciones", direcciones)
        print("distinguir", distinguir)
        print("identificaciones", identificaciones)
        print(colSenDer.value(0), colSenDer.value(1), colSenDer.value(2))

    while run2 == True:
        
        for col in colores:
            if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                valor = abs(sum(
                    colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                distinguir = col
        valor = 100

        if ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumafueral)) < 10):
            distinguir = "afueral"
        
        if ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumazulrampa)) < 10):
            distinguir = "azulrampa"

        if (distinguir == "azulrampa"):
            
            alinearseiniciocuidado()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa1 = col
            valor = 100
            avanzar3cm()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(
                        colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa2 = col
            valor = 100

            if (rampa1 == "rojo") & (rampa2 != "rojo"):

                if cargamento == True:
                    avanzarpor15cm()
                    run2 = False
                    run4 = True

                if cargamento == False:
                    avanzarpor5cmreversa
                    girar90GradosIzquierda()
                    motoresTanqueGirar.on_for_seconds(-10, -10, 0, brake=True, block=True)
                    girar90GradosIzquierda()
                    run2 = False
                    run3 = True
                    direcciones[0] = direcciones[0] * (-1)
                    direcciones[1] = direcciones[1] * (-1)
                    direcciones[2] = direcciones[2] * (-1)

        if (distinguir == "afueral"):
            avanzar3cmreversa()
            minigiroder()

        if (distinguir == "afuera"):
            avanzar3cmreversa()
            minigiroizq()

        if (distinguir == "blanco"):
            if cargamento == False:
                if (usDer.value() > rango) & (usIzq.value() > rango):
                    avanzarporsiempre()

                if (usDer.value() < rango):
                    motoresTanqueGirar.on_for_seconds(10, 10, 1.2, brake=True, block=True)
                    recogerMonoDerecha()
                    monos = monos + 1

                if (usIzq.value() < rangoizq):
                    motoresTanqueGirar.on_for_seconds(10, 10, 1.2, brake=True, block=True)
                    recogerMonoIzquierda()
                    monos = monos + 1

                if monos == 2:
                    cargamento = True
            if cargamento == True:
                avanzarporsiempre()

        if (distinguir == "negro"):
            alinearseinicio()

        if (distinguir == "rojo"):
            alinearseiniciocuidado()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa1 = col
            valor = 100
            avanzar3cm()
            avanzar3cm()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa2 = col
            valor = 100

            if (rampa1 == "rojo") & (rampa2 != "rojo") :

                if cargamento == True:
                    avanzarpor15cm()
                    avanzarpor15cm()

                    run2 = False
                    run4 = True

                if cargamento == False:
                    avanzarpor5cmreversa
                    girar90GradosIzquierda()
                    motoresTanqueGirar.on_for_seconds(-10, -10, 0, brake=True, block=True)
                    girar90GradosIzquierda()
                    run2 = False
                    run3 = True
                    direcciones[0] = direcciones[0] * (-1)
                    direcciones[1] = direcciones[1] * (-1)
                    direcciones[2] = direcciones[2] * (-1)


            if rampa2 == "rojo":
                avanzarpor5cmreversa

                if direcciones[0] == -1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

                if direcciones[0] == 0:
                    alinearseinicio()
                    avanzarpor30cm()
                    alinearse()

                if direcciones[0] == 1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosDerecha()
                    alinearse()

        if (distinguir == "verde"):
            alinearseiniciocuidado()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa1 = col
            valor = 100
            avanzar3cm()
            for col in colores:
                if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                    valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                    rampa2 = col
            valor = 100

            if (rampa1 == "rojo") & (rampa2 != "rojo") :

                if cargamento == True:
                    avanzarpor15cm()
                    avanzarpor15cm()
                    run2 = False
                    run4 = True

                if cargamento == False:
                    avanzarpor5cmreversa
                    girar90GradosIzquierda()
                    motoresTanqueGirar.on_for_seconds(-10, -10, 0, brake=True, block=True)
                    girar90GradosIzquierda()
                    run2 = False
                    run3 = True
                    direcciones[0] = direcciones[0] * (-1)
                    direcciones[1] = direcciones[1] * (-1)
                    direcciones[2] = direcciones[2] * (-1)

            if (rampa1 == "verde") & (rampa2 == "verde"):
                avanzarpor5cmreversa

                if direcciones[1] == -1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosIzquierda()
                    alinearse()

                if direcciones[1] == 0:
                    alinearseinicio()
                    avanzarpor30cm()
                    alinearse()

                if direcciones[1] == 1:
                    alinearseinicio()
                    avanzarpor15cm()
                    girar90GradosDerecha()
                    alinearse()

        if (distinguir == "azul"):

            if direcciones[2] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

            if direcciones[2] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

            if direcciones[2] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

    while run3 == True:
        for col in colores:
            if (abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < valor):
                valor = abs(sum(colores[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
                distinguir = col
        valor = 100

        if ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumafueral)) < 10):
            distinguir = "afueral"

        if (distinguir == "afueral"):
            avanzar3cmreversa()
            minigiroder()

        if (distinguir == "afuera"):
            avanzar3cmreversa()
            minigiroizq()

        if (distinguir == "blanco"):
            if cargamento == False:
                
                if (usDer.value() > rango) & (usIzq.value() > rango):
                    avanzarporsiempre()

                if (usDer.value() < rango):
                    motoresTanqueGirar.on_for_seconds(10, 10, 1.2, brake=True, block=True)
                    recogerMonoDerecha()
                    monos = monos + 1

                if (usIzq.value() < rangoizq):
                    motoresTanqueGirar.on_for_seconds(10, 10, 1.2, brake=True, block=True)
                    recogerMonoIzquierda()
                    monos = monos + 1

                if monos == 2:
                    cargamento = True

            if cargamento == True:
                avanzarpor5cmreversa
                girar90GradosIzquierda()
                motoresTanqueGirar.on_for_seconds(-10, -10, 0, brake=True, block=True)
                girar90GradosIzquierda()
                run2 = True
                run3 = False
                direcciones[0] = direcciones[0] * (-1)
                direcciones[1] = direcciones[1] * (-1)
                direcciones[2] = direcciones[2] * (-1)

        if (distinguir == "negro"):
            #color="negro"
            alinearseinicio()
            avanzar3cm()

        if (distinguir == "rojo"):
            
            if direcciones[0] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

            if direcciones[0] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

            if direcciones[0] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

        if (distinguir == "verde"):

            if direcciones[1] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

            if direcciones[1] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

            if direcciones[1] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()

        if (distinguir == "azul"):

            if direcciones[2] == -1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosIzquierda()
                alinearse()

            if direcciones[2] == 0:
                alinearseinicio()
                avanzarpor30cm()
                alinearse()

            if direcciones[2] == 1:
                alinearseinicio()
                avanzarpor15cm()
                girar90GradosDerecha()
                alinearse()
    
    while run4 == True:
        dejarMonos()
        alinearse()
        monos = 0
        cargamento = False
        run3 = True
        run4 = False
