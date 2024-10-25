#!/usr/bin/env pybricks-micropython

#imports das bibliotecas necessárias
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, InfraredSensor,ColorSensor
from pybricks.parameters import Port, Direction,Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint

#criação de uma instancia do módulo principal 
ev3= EV3Brick()

#inicialização dos motores
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.D)

colorSensor = ColorSensor(Port.S2)

def color():
    contador = 0
    while contador < 10:
        if colorSensor.color() == Color.YELLOW:
            middle_motor.run(1000)
            wait(1000)
            middle_motor.stop()
            ev3.speaker.beep(400, 100)  # C
            wait(100)
            ev3.speaker.beep(400, 100)  # C
            wait(100)
            ev3.speaker.beep(470, 100)  # C
            wait(100)
            middle_motor.run(-1000)
            wait(1000)
            middle_motor.stop()
        contador += 1
    
'''
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
'''
#cor barreiras -> vermelho
#cor linhas -> preto
#cor manteiga -> amarelo

while True:
    print(cor=colorSensor.color())
    #Se o sensor de cor detectar a cor preta, o robô andará para frente
    if colorSensor.color() == colorSensor.COLOR_BLACK:
        speed = 500
        left_motor.run(speed)
        right_motor.run(speed)
        wait(5000)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar outra cor, da uma volta 
    elif colorSensor.color() == None :
        left_motor.run_angle(1000,-900)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar a cor vermelha/barreira, o robô dará uma volta
    elif colorSensor.color() == colorSensor.COLOR_RED :
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()
    elif colorSensor.color() == colorSensor.COLOR_BROWN:
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()

# movimento

speed = 250
direcao = ""

def andar():
    left_motor.run(speed/2)
    right_motor.run(speed/2)
    wait(3700)
    if colorSensor.color()== Color.RED:
        left_motor.stop()
        right_motor.stop()
        left_motor.run(-speed/2)
        right_motor.run(-speed/2)
        wait(1850)
        left_motor.stop()
        right_motor.stop()
        rodar_direita()
    wait(3800)
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
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    right_motor.run_angle(1000, 700)
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    if direcao == "frente":
        direcao = "direita"
    if direcao == "direita":
        direcao = "atras"
    if direcao == "atras":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "frente"

def rodar_esquerda():
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    left_motor.run_angle(1000, 700)
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    if direcao == "frente":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "atras"
    if direcao == "atras":
        direcao = "direita"
    if direcao == "direita":
        direcao = "frente"