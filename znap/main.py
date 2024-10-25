#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, InfraredSensor,ColorSensor
from pybricks.parameters import Port, Direction,Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint


#------------------------------------------------------------------------------------------------------> 
#                                       inicializações 
#--------------------------------------------------------------------------------------->
#criação de uma instancia do módulo principal 
ev3= EV3Brick()

#inicialização dos motores
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.D)

#inicialização do sensor de cor
colorSensor = ColorSensor(Port.S2)

#cor barreiras -> vermelho
#cor linhas -> preto
#cor manteiga -> amarelo
#cor torradeira -> azul 

#------------------------------------------------------------------------------------------------------> 
#                                    Detetar Manteiga e a agarrar

# e frequência de aviso que agarrou a manteiga
#------------------------------------------------------------------------------------------------------> 

def Deteta_agarra_manteiga():
    if colorSensor.color() == Color.YELLOW:
        #Desenha na tela do ev3
        ev3.screen.draw_text(50, 60, "Manteiga Detetada!")

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
    else  
        ev3.screen.draw_text(50, 60, "Á procura da Manteiga")   

        
    
#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

localizacao = [1,1] #localização inicial
direcao = "frente"  #direção inicial
speed = 250 #velocidade inicial 

def podeAndar(direcao):
    if(localizacao[0] == 1 and direcao == "esquerda"):
        return False
    if(localizacao[1] == 6 and direcao == "frente"):
        rcalizacao[]eturn False
    if(localizacao[0] == 6 and direcao == "direita"):
        return False
    if(l)

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