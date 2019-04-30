#!/usr/bin/env python3
# So program can be run from Brickman


# <--Importar librerías-->

from ev3dev.ev3 import *
from time import sleep, time
import os
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.motor import SpeedRPM, SpeedRPS, SpeedDPM, MoveTank, MoveSteering

os.system('setfont Lat15-TerminusBold14')

# <--Parámetros-->
coloresDer = {"afuera": [(8, 5, 7),'sentido'],"negro": [(26, 24, 30), "sentido"], "blanco": [(257, 281, 249), "sentido"],
              "rojo": [(167, 28, 33), "sentido"], "azul": [(267, 158, 51), "sentido"],
              "verde": [(32, 48, 30), "sentido"],
              "azulRampa": [(33, 93, 166), "sentido"]}

coloresIzq = {"afuera": [(11, 8, 4), "sentido"],"negro": [(26, 35, 14), "sentido"], "blanco": [(286, 305, 149), "sentido"],
              "rojo": [(194, 39, 16), "sentido"], "azul": [(302, 170, 30), "sentido"],
              "verde": [(39, 57, 16), "sentido"],
               "azulRampa": [(47, 139, 104), "sentido"]}

# <---Puertos--->

# --Sensor Ultrasonico--
usIzq = UltrasonicSensor('in3')
usIzq.mode = 'US-DIST-CM'
unitsIzq = usIzq.units
distanceIzq = usIzq.value()  # convert mm to cm

usDer = UltrasonicSensor('in4')
usDer.mode = 'US-DIST-CM'
unitsDer = usDer.units
distanceDer = usDer.value()  # convert mm to cm

# --Motores--
MotIzq = LargeMotor('outB')  # Motor Izquierdo
MotDer = LargeMotor('outA')  # Motor derecho
MotBzo = LargeMotor('outD')  # Motor de brazo
motoresTanqueGirar = MoveTank(OUTPUT_B, OUTPUT_A)  # Concatena los 2 motores para usar funciones de giro y grados
motoresTanqueRotaciones = MoveSteering(OUTPUT_B, OUTPUT_A)  # Concatena los 2 motores para usar funciones de tiempo

# --Sensor de color--
colSenDer = ColorSensor('in1')
colSenIzq = ColorSensor('in2')
colSenDer.mode = 'RGB-RAW'
colSenIzq.mode = 'RGB-RAW'


def girar90GradosDerecha():
    motoresTanqueGirar.on_for_degrees(15, -15, 437, brake=True, block=True)

def girar90GradosIzquierda():
    motoresTanqueGirar.on_for_degrees(-15, 15, 437, brake=True, block=True)

def levantarBrazo():
    MotBzo.on_for_rotations(-50, .4)
    MotBzo.stop(stop_action="hold")

def bajarBrazo():
    MotBzo.on_for_rotations(50, .5)
    MotBzo.stop(stop_action="hold")

def stopRobotAtPerson():
    distanceIzq = usIzq.value()
    distanceDer = usDer.value()
    if distanceIzq < 15:
        return -1
    elif distanceDer < 15:
        return 1
    return 0

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
    direccion = stopRobotAtPerson()
    motoresTanquePair.off(brake=True)
    if direccion == -1:
        recogerMonoIzquierda()
    else:
        recogerMonoDerecha()
    return direccion ** 2


def avanzarCentroCuadro(color):
    if color == 'negro':
        motoresTanqueGirar.off(brake=True)
    else:
        motoresTanqueGirar.on_for_seconds(30, 30, 1.5, brake=True, block=True)


def obtenerColorDer():
    error = 100
    color = 'afuera'
    for col in coloresDer:
        if (abs(sum(coloresDer[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)])) < error):
            error = abs(sum(coloresDer[col][0]) - sum([colSenDer.value(0), colSenDer.value(1), colSenDer.value(2)]))
            color = col
    if error < 100:
        return color
    return 'afuera'


def obtenerColorIzq():
    error = 100
    color = 'afuera'
    for col in coloresIzq:
        if (abs(sum(coloresIzq[col][0]) - sum([colSenIzq.value(0), colSenIzq.value(1), colSenIzq.value(2)])) < error):
            error = abs(sum(coloresIzq[col][0]) - sum([colSenIzq.value(0), colSenIzq.value(1), colSenIzq.value(2)]))
            color = col
    if error < 100:
        return color
    return 'afuera'


def vacioIzq(colorIzq):
    if colorIzq == 'vacio':
        motoresTanqueGirar.on_for_rotations(40, 0, .3)


def vacioDer(colorDer):
    if colorDer == 'vacio':
        motoresTanqueGirar.on_for_rotations(0, 40, .3)


def alinearseEntrada():
    colorIzq = obtenerColorIzq()
    colorDer = obtenerColorDer()
    motoresTanqueGirar.on_for_rotations(-20, -20, .4)
    while colorIzq == 'blanco':
        motoresTanqueGirar.on(30, 25)
        colorIzq = obtenerColorIzq()
    while colorDer == 'blanco':
        motoresTanqueGirar.on(0, 10)
        colorDer = obtenerColorDer()


def alinearseSalida():
    colorIzq = obtenerColorIzq()
    colorDer = obtenerColorDer()
    while coloresIzq != 'blanco':
        motoresTanqueGirar.on(40, 40)
        vacioIzq(coloresIzq)
        vacioDer(colorDer)
        colorIzq = obtenerColorIzq()
        colorDer = obtenerColorDer()
    motoresTanqueGirar.on_for_rotations(20, 20, .3)
    while colorIzq == 'blanco':
        motoresTanqueGirar.on(-30, -25)
        colorIzq = obtenerColorIzq()
    while colorDer == 'blanco':
        motoresTanqueGirar.on(0, -10)
        colorDer = obtenerColorDer()
    motoresTanqueGirar.on_for_rotations(20, 20, .5)


def avanzarSigColor():
    colorIzq = obtenerColorIzq()
    colorDer = obtenerColorDer()
    while (coloresIzq == 'blanco' or coloresIzq == 'vacio') and (colorDer == 'blanco' or colorDer == 'vacio'):
        vacioIzq(colorIzq)
        vacioDer(vacioDer)
        motoresTanqueGirar.on(50, 50)
        colorIzq = obtenerColorIzq()
        colorDer = obtenerColorDer()
    alinearseEntrada()
    avanzarCentroCuadro(coloresIzq)
    return colorIzq


def alinearseRampa():
    colorIzq = obtenerColorIzq()
    colorDer = obtenerColorDer()
    while coloresIzq != 'verde':
        motoresTanqueGirar.on(10,10)
    alinearseSalida()
    


def detectarRampa(color):
    motoresTanqueGirar.on_for_rotations(20, 20, .3)
    colorIzq = obtenerColorIzq()
    if colorIzq == color:
        return False
    else:
        alinearseRampa()
    return True


def avanzarSigColorDespuesMapeado(monos_recogidos):
    colorIzq = obtenerColorIzq()
    colorDer = obtenerColorDer()
    while (coloresIzq == 'blanco' or coloresIzq == 'vacio') and (colorDer == 'blanco' or colorDer == 'vacio'):
        vacioIzq(colorIzq)
        vacioDer(vacioDer)
        if monos_recogidos < 2:
            monos_recogidos += recogerMono()
        else:
            monos_recogidos += 0
        motoresTanqueGirar.on(50, 50)
        colorIzq = obtenerColorIzq()
        colorDer = obtenerColorDer()
    alinearseEntrada()
    rampa = detectarRampa(colorIzq)
    if rampa:
        avanzarCentroCuadro(coloresIzq)
    return [colorIzq, monos_recogidos, rampa]


def identificarSentidoColor(colorCuadroLlegada):
    for intento in range(1, 4):
        girar90GradosIzquierda()
        colorCuadro = avanzarSigColor()
        if colorCuadro != 'negro' and colorCuadro != 'afuera':
            if intento == 1:
                coloresIzq[colorCuadroLlegada][1] = 'izq'
            elif intento == 2:
                coloresIzq[colorCuadroLlegada][1] = 'cen'
            else:
                coloresIzq[colorCuadroLlegada][1] = 'der'
            alinearseSalida()
            break
        motoresTanqueGirar.on_for_rotations(-40, -40, .7)
        girar90GradosDerecha()
        girar90GradosDerecha()
        color = avanzarSigColor()
        avanzarCentroCuadro(color)


def mapearPista():
    colorCuadroLlegada = avanzarSigColor()
    while coloresIzq['rojo'][1] == 'sentido' or coloresIzq['azul'][1] == 'sentido' or coloresIzq['verde'][1] == 'sentido':
        colorCuadroLlegada = identificarSentidoColor(colorCuadroLlegada)
    return True


def salirFuerza():
    girar90GradosIzquierda()
    motoresTanqueGirar.off(brake=True)
    motoresTanqueGirar.on_for_rotations(-50, -50, 5)
    motoresTanqueGirar.on_for_rotations(50, 50, .6)
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
    while not salio and not atorado:
        colorDer = obtenerColorDer()
        colorIzq = obtenerColorIzq()
        motoresTanqueGirar.on_for_rotations(50, 50, .9)
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
        motoresTanqueGirar.on(50, 50)
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
    motoresTanqueGirar.on_for_rotations(50, 50, 1)


def recorrerPista():
    rampa = False  # Hacer funcion para detectar rampa
    monos_recogidos = 0
    while not rampa:
        cuadroDespuesMapeado = avanzarSigColorDespuesMapeado()
        colorSiguienteCuadroDespuesMapeado = cuadroDespuesMapeado[0]
        monos_recogidos += cuadroDespuesMapeado[1]
        rampa = cuadroDespuesMapeado[2]
        if coloresIzq[colorSiguienteCuadroDespuesMapeado][1] == 'izq':
            girar90GradosIzquierda()
        elif coloresIzq[colorSiguienteCuadroDespuesMapeado][1] == 'der':
            girar90GradosDerecha()
        alinearseSalida()
    dejarMonos()


def main():

    mapearPista()
    while True:
        recorrerPista()
        dejarMonos()

while True:
    print(obtenerColorIzq(),obtenerColorDer())
    

