#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, UltrasonicSensor,ColorSensor
from pybricks.parameters import Port, Direction,Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint


#------------------------------------------------------------------------------------------------------> 
#                                       inicializações 
#------------------------------------------------------------------------------------------------------>
#criação de uma instancia do módulo principal 
ev3= EV3Brick()

#inicialização dos motores
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.D)

#inicialização do sensor de cor
colorSensor = ColorSensor(Port.S2)
distanciaSensor = UltrasonicSensor(Port.S1)
#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 
#------------------------------------------------------------------------------------------------------> 
#                                    dETE
#------------------------------------------------------------------------------------------------------> 
def color():
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
    

#cor barreiras -> vermelho
#cor linhas -> preto
#cor manteiga -> amarelo
#cor torradeira -> azul 

#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

localizacao = [1,1] #localização inicial
direcao = "frente"
dirCode = 1 #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras
speed = 250
nextDir = "" #proxima direção
nextDirCode = 0 #código da proxima 

def podeAndar(direcao): #função que verifica se é possível andar na direção indicada
    if localizacao[0] == 1 and direcao == "esquerda":
        return False
    elif localizacao[1] == 6 and direcao == "frente":
        return False
    elif localizacao[0] == 6 and direcao == "direita":
        return False
    elif localizacao[1] == 1 and direcao == "atras":
        return False
    else:
        return True

def modulo(a):
    if a < 0:
        return -a
    else:
        return a



def andar(nextDir):
    if podeAndar(nextDir):
        if modulo(nextDirCode - dirCode) == 1:
            if nextDir == "esquerda":
                rodar_esquerda()
            else:
                rodar_direita()
        elif modulo(nextDir - dirCode) == 2:
            rodar_direita()
            rodar_direita()

        left_motor.run(speed/2)
        right_motor.run(speed/2)
        wait(3700)
            colorSensor.color()== Color.RED:
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
            direcao == "frente":
            localizacao[1] += 1
            direcao == "direita":
            localizacao[0] += 1
            direcao == "atras":
            localizacao[1] -= 1
            direcao == "esquerda":
            localizacao[0] -= 1
            color()
    else:
        ev3.speaker.beep(400, 100)

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
        dirCode = 3
    if direcao == "direita":
        direcao = "atras"
        dirCode = 4
    if direcao == "atras":
        direcao = "esquerda"
        dirCode = 1
    if direcao == "esquerda":
        direcao = "frente"
        dirCode = 2

#------------------------------------------------------------------------------------------------------> 
# Função rodar_esquerda 
#------------------------------------------------------------------------------------------------------>
def rodar_esquerda():
    left_motor.run(-speed*2) #
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

#------------------------------------------------------------------------------------------------------> 
# Função randDir retorna a próxima direção 
#------------------------------------------------------------------------------------------------------>
def randDir():
    nextDirCode = randint(4) + 1 # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5  if nextDirCode == 2:
        nextDir = "frente"        # norte 
    if nextDirCode == 1:
        nextDir = "esquerda"      #
    if nextDirCode == 3:
        nextDir == "direita"
    if nextDirCode == 4:
        nextDir == "atras"
    return nextDir

while True:
    #andar(randDir())
    print(distanciaSensor.distance(silent=False))