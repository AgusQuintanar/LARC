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
negro = (32, 41, 15)
afueral = (19, 21, 11)
afuera = (26, 25, 13)
blanco = (307, 309, 152)
blancol = (259, 284, 148)
rojo = (263, 53, 18)
azul = (322, 233, 33)
verde = (38, 93, 25)
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
    motoresTanqueGirar.on_for_degrees(15, -15, 475, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 430, brake=True, block=True)

def avanzarporsiempre():
    motoresTanqueGirar.on(15, 15)

def avanzarporsiemprederecha():
    motoresTanqueGirar.on(15, 0)

def avanzarporsiempreizquierda():
    motoresTanqueGirar.on(0, 15)

def avanzarporsiemprederechareversa():
    motoresTanqueGirar.on(-10, 0)

def avanzarporsiempreizquierdareversa():
    motoresTanqueGirar.on(0, -10)

def avanzarporsiemprereversa():
    motoresTanqueGirar.on(-10, -10)

def avanzarpor15cmreversa():
    motoresTanqueGirar.on_for_seconds(-30, -30, 1.4, brake=True, block=True)

def avanzarpor15cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 1.4, brake=True, block=True)

def avanzarpor30cm():
    motoresTanqueGirar.on_for_seconds(30, 30, 2, brake=True, block=True)

def avanzarpor1cm():
    avanzarporsiempre()
    #motoresTanqueGirar.on_for_seconds(30, 30, 0.5, brake=True, block=True)

def avanzarpor5cm():
    motoresTanqueGirar.on_for_seconds(15, 15, 1.6, brake=True, block=True)

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

    if (colSenDer.value(0) > colSenDer.value(1)) & (colSenDer.value(0) > colSenDer.value(2)):
        mayor = 0
    
    if (colSenDer.value(1) > colSenDer.value(2)) & (colSenDer.value(1) > colSenDer.value(0)):
        mayor = 1

    if (colSenDer.value(2) > colSenDer.value(1)) & (colSenDer.value(2) > colSenDer.value(0)):
        mayor = 2
    
    if mayor == 0:
        if ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumrojo)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumafuera))) & ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumrojo)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumazul))):
            distinguir = "rojo"

        if (((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumafuera)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumrojo))) & ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumafuera)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumazul)))) | ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumafueral)) < 10):
            distinguir = "afuera"

        if ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumazul)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumrojo))) & ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-sumazul)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumafuera))):
            distinguir = "azul"

    if mayor == 1:

        if ((abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumblanco)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumnegro))) & (abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumblanco)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumverde)))):
            distinguir = "blanco"

        if (abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumnegro)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumblanco))) & (abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2)-(sumnegro)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2)-(sumverde))))):
            distinguir = "negro"
        
        if (abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumverde)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumblanco))) & (abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumverde)) < abs((colSenDer.value(0)+colSenDer.value(1)+colSenDer.value(2))-(sumnegro))):
            distinguir = "verde"
        if ((abs((colSenIzq.value(0)+colSenIzq.value(1)+colSenIzq.value(2))-sumafueral)) < 10):
            distinguir = "afuera"
            
    if (distinguir == "afuera"):
        #función para que no se salga
        avanzarpor15cmreversa()

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
        if direcciones[0] == 0:
            avanzarpor30cm()
            alinearse()
        if direcciones[0] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()
        if direcciones[0] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()
            if intento == 0 :
                intento =  intento + 1
                color = "rojo"
            if intento == 1:
                if color == "rojo":
                    direcciones[0]=-1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 1
                color = "rojo"
                identificaciones = identificaciones + 1
            if intento == 2:
                intento = intento + 1
            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 1
                color = "rojo"
                identificaciones = identificaciones + 1
            if intento == 4:
                intento = intento + 1
            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 1
                color = "rojo"
                identificaciones = identificaciones + 1

    if (distinguir == "verde"):
        if direcciones[1] == -1:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()
        if direcciones[1] == 0:
            avanzarpor30cm()
            alinearse()
        if direcciones[1] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()
        if direcciones[1] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()
            if intento == 0:
                intento = intento + 1
                color = "verde"
            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                
                color = "verde"
                identificaciones = identificaciones + 1
            if intento == 2:
                intento = intento + 1
            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
             
                color = "verde"
                identificaciones = identificaciones + 1
            if intento == 4:
                intento = intento + 1
            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 1
                color = "verde"
                identificaciones = identificaciones + 1

    if (distinguir == "azul"):
        if direcciones[2] == -1:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()
        if direcciones[2] == 0:
            avanzarpor30cm()
            alinearse()
        if direcciones[2] == 1:
            avanzarpor15cm()
            girar90GradosDerecha()
            alinearse()
        if direcciones[2] == 2:
            avanzarpor15cm()
            girar90GradosIzquierda()
            alinearse()
            if intento == 0:
                intento = intento + 1
                color = "azul"
            if intento == 1:
                if color == "rojo":
                    direcciones[0] = -1
                if color == "verde":
                    direcciones[1] = -1
                if color == "azul":
                    direcciones[2] = -1
                intento = 1
                color = "azul"
                identificaciones = identificaciones + 1
            if intento == 2:
                intento = intento + 1
            if intento == 3:
                if color == "rojo":
                    direcciones[0] = 0
                if color == "verde":
                    direcciones[1] = 0
                if color == "azul":
                    direcciones[2] = 0
                intento = 1
                color = "azul"
                identificaciones = identificaciones + 1
            if intento == 4:
                intento = intento + 1
            if intento == 5:
                if color == "rojo":
                    direcciones[0] = 1
                if color == "verde":
                    direcciones[1] = 1
                if color == "azul":
                    direcciones[2] = 1
                intento = 1
                color = "azul"
                identificaciones = identificaciones + 1
    if identificaciones == 3:
        run = False
    print(color)
    print(intento)
    print(direcciones)
    print(distinguir)