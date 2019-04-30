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

colores = {"negro": [(30, 40, 14), 0], "blanco": [(308, 319, 153), 0], "rojo": [(263, 52, 16), 0], "azul": [(319, 235, 32), 0], "verde": [(35, 93, 24), 0], "afuera": [(20, 19, 11), 0]}
negro = (28, 35, 15)
afueral = (18, 19, 10)
afuera = (23, 22, 13)
blanco = (289, 304, 148)
blancol = (253, 285, 148)
rojo = (253, 45, 17)
azul = (306, 225, 33)
verde = (35, 95, 26)
run1 = True
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


#<---Puertos--->

#--Sensor Ultrasonico--
usIzq = UltrasonicSensor('in3') 
usIzq.mode='US-DIST-CM'
units = usIzq.units                                                                                                            
distance = usIzq.value()  # convert mm to cm

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


#<--Funciones-->

#def obtenerColor():
#    return [colors[colSenDer.value()],colors[colSenIzq.value()]]
       
"""def noSalirse():
    if obtenerColor()[0] == 'unknown':
        MotIzq.stop("hold")
        delay(.8)
        MotDer.on_for_seconds(10, 1)
    
        MotIzq.stop("hold")

    elif obtenerColor()[1] == 'unknown':
        MotDer.on_for_seconds(5, .3)
        sleep(1)
        MotIzq.on_for_seconds(10, 1)"""

def levantarBrazo():
    MotBzo.on_for_rotations(-50, .4)

def bajarBrazo():
    MotBzo.on_for_rotations(40, .38)

def stopRobotAtPerson(distance):
    while distance>30:   
        print(str(distance) + " " + units)
        MotIzq.run_forever(500)
        MotDer.run_forever(500)
        #noSalirse()
        distance = usIzq.value()  # convert mm to cm

    MotIzq.stop("hold")
    MotDer.stop("hold")

def recogerMono():
    stopRobotAtPerson(distance)
    levantarBrazo()
    girar90GradosIzquierda()

def girar90GradosDerecha():
    motoresTanqueGirar.on_for_degrees(15, -15, 430, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 430, brake=True, block=True)

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
    motoresTanqueGirar.on(15, 15)

def avanzarporsiemprederecha():
    motoresTanqueGirar.on(10, 0)

def avanzarporsiempreizquierda():
    motoresTanqueGirar.on(0, 10)

def avanzarporsiemprederechareversa():
    motoresTanqueGirar.on(-10, 0)

def avanzarporsiempreizquierdareversa():
    motoresTanqueGirar.on(0, -10)

def avanzarporsiemprereversa():
    motoresTanqueGirar.on(-10, -10)

def avanzarpor15cmreversa():
    motoresTanqueGirar.on_for_seconds(-30, -30, 1.3, brake=True, block=True)

def avanzarpor15cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 1.25, brake=True, block=True)

def avanzarpor30cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 2, brake=True, block=True)

def avanzarpor1cm():
    avanzarporsiempre()
    #motoresTanqueGirar.on_for_seconds(30, 30, 0.5, brake=True, block=True)

def avanzarpor5cm():
    motoresTanqueGirar.on_for_seconds(15, 15, 1.6, brake=True, block=True)

def avanzar3cmreversa():
    motoresTanqueGirar.on_for_seconds(-15, -15, 0.6, brake=True, block=True)

def minigiroizq():
    motoresTanqueGirar.on_for_degrees(-15, 15, 110, brake=True, block=True)

def minigiroder():
    motoresTanqueGirar.on_for_degrees(15, -15, 110, brake=True, block=True)

def alinearse():
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
            avanzarpor5cm()
            continuar = "si"


#<--Programa-->

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
        girar90GradosIzquierda()
        girar90GradosIzquierda()
        intento = intento + 1


    if (distinguir == "rojo"):
        
        if direcciones[0] == -1:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[0] == 0:
            avanzarpor30cm()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[0] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[0] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0
                color = "rojo"
                identificaciones = identificaciones + 1

            if intento == 4:
                intento = intento +1

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0
                color = "rojo"
                identificaciones = identificaciones + 1

            if intento == 2:
                intento = intento + 1

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0
                color = "rojo"
                identificaciones = identificaciones + 1

            if intento == 0:
                intento = 1
                color = "rojo"

    if (distinguir == "verde"):
        
        if direcciones[1] == -1:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[1] == 0:
            avanzarpor30cm()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[1] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[1] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0
                color = "verde"
                identificaciones = identificaciones + 1

            if intento == 4:
                intento = 5

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0
                color = "verde"
                identificaciones = identificaciones + 1

            if intento == 2:
                intento = 3

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0
                color = "verde"
                identificaciones = identificaciones + 1

            if intento == 0:
                intento = 1
                color = "verde"

    if (distinguir == "azul"):

        if direcciones[2] == -1:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[2] == 0:
            avanzarpor30cm()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[2] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0

        if direcciones[2] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()

            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 0
                color = "azul"
                identificaciones = identificaciones + 1

            if intento == 4:
                intento = 5

            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 0
                color = "azul"
                identificaciones = identificaciones + 1

            if intento == 2:
                intento = 3

            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 0
                color = "azul"
                identificaciones = identificaciones + 1

            if intento == 0:
                intento = 1
                color = "azul"

    if (identificaciones==6):
        run1 = False

    print("color", color)
    print("intento", intento)
    print("direcciones", direcciones)
    print("distinguir", distinguir)
    print("identificaciones", identificaciones)
    print(colSenDer.value(0), colSenDer.value(1), colSenDer.value(2))
