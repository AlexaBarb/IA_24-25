#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Znap Program
------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-expansion
"""
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint

ev3= EV3Brick()
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.A)

'''
middle_motor.run(1000)
wait(2000)
middle_motor.stop()

i = 0
while i < 2:
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(300, 250)  # D
    wait(200)
    ev3.speaker.beep(400, 100)  # E
    wait(250)
    i = i + 1

# Parte final da música
wait(100)
ev3.speaker.beep(400, 200)  # F
wait(200)
ev3.speaker.beep(400, 100)  # F
wait(100)
ev3.speaker.beep(350, 100)  # D
wait(100)
ev3.speaker.beep(350, 100)  # D
wait(100)
ev3.speaker.beep(300, 100)  # D
wait(100)
ev3.speaker.beep(300, 100)  # D
wait(100)
ev3.speaker.beep(200, 150)  # G
#FAZER MOVIMENTO
left_motor.run_angle(1000,-900)
speed = 500
left_motor.run(speed)
right_motor.run(speed)
wait(5000)
left_motor.stop()
right_motor.stop()
left_motor.run_angle(1000,900)

#MOVER A GARRA
middle_motor.run(-1000)
wait(2000)
middle_motor.stop()
'''

# Lista que armazenará os símbolos associados às cores detetadas (por exemplo, "+", "*", etc.).
pecas = []
ev3 = EV3Brick() 

# Sensor de cor
sensorCor = ColorSensor(Port.S1) 

# Deteta a cor passada no sensor de cores
def detetaCor():
    # Lê o valor da cor
    corDetetada = sensorCor.color()

    # Mapa de valores de cor para nomes de cor
    listaCores = {
        Color.BLUE: 'Azul',
        Color.GREEN: 'Verde',
        Color.YELLOW: 'Amarelo',
        Color.RED: 'Vermelho',
    }

    # Determina a cor detectada
    nomeCorDetetada = listaCores.get(corDetetada, 'Desconhecida')
    # Retorna o nome da cor detectada
    return nomeCorDetetada

# Deteta a cor das peças passadas e adiciona no array das peças
def detetaCorPecas():
    # Lê o nome da cor
    corDetetada = detetaCor()
    # Imprime a cor lida
    print('Cor detectada: ' + corDetetada)

    # Adiciona a peça no array dependendo da cor
    if corDetetada == 'Verde':
        pecas.append("+")
        ev3.speaker.say("Green")
        
    elif corDetetada == 'Vermelho':
        pecas.append("*")
        ev3.speaker.say("Red")
        
    elif corDetetada == 'Amarelo':
        pecas.append("0")
        ev3.speaker.say("Yellow")
        
    elif corDetetada == 'Azul':
        pecas.append("-")
        ev3.speaker.say("Blue")

# Período da deteção de peças            
def leituraObjetos():
    # Enquanto está no período de deteção
    while True:
        # Deteta e guarda as peças
        detetaCorPecas()
        # Espera 2 segundos
        wait(2000)

localizacao = [1,1]
direcao = "frente"

Cor_Sensor = ColorSensor(Port.S1)

#cor barreiras -> vermelho
#cor linhas -> preto
#cor limitação de ambiente -> verde
while True:
    print(Cor_Sensor.color())
    #Se o sensor de cor detectar a cor preta, o robô andará para frente
    if datetaCor() == Cor_Sensor.COLOR_BLACK:
        speed = 500
        left_motor.run(speed)
        right_motor.run(speed)
        wait(5000)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar outra cor, da uma volta 
    elif datetaCor() == None :
        left_motor.run_angle(1000,-900)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar a cor vermelha/barreira, o robô dará uma volta
    elif datetaCor() == Cor_Sensor.COLOR_RED :
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()
    elif datetaCor() == Cor_Sensor.COLOR_BROWN:
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()

# movimento

speed = 500

def andar():
    left_motor.run(speed)
    right_motor.run(speed)
    wait(1850)
    left_motor.stop()
    right_motor.stop()
    if direcao == "frente":
        localizacao[1] += 1
    if direcao == "direita":
        localizacao[0] += 1
    if direcao == "atras":
        localizacao[1] -= 1
    if direcao == "esquerda":
        localizacao[0] -= 1

def rodar_direita():
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    left_motor.run_angle(1000, -680)
    if direcao == "frente":
        direcao = "direita"
    if direcao == "direita":
        direcao = "atras"
    if direcao == "atras":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "frente"

def rodar_esquerda():
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    right_motor.run_angle(1000, -680)
    if direcao == "frente":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "atras"
    if direcao == "atras":
        direcao = "direita"
    if direcao == "direita":
        direcao = "frente"

leituraObjetos()
print(detetaCorPecas())

andar()
wait(2000)
rodar_direita()
wait(1000)
andar()
wait(1000)
rodar_esquerda()