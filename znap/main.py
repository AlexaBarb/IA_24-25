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
        # Limpar a tela antes de desenhar
        ev3.screen.clear()
        ev3.screen.draw_text(50, 60, "YAY Manteiga encontrada")
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
    else:
        # Limpar a tela antes de desenhar
        ev3.screen.clear()
        ev3.screen.draw_text(50, 60, "A procura da Mant")

def emoji_triste():
        # Limpar a tela antes de desenhar
        ev3.screen.clear()

        # Desenhar os olhos (círculos)
        # Olho esquerdo
        ev3.screen.draw_circle(60, 50, 10, fill=True)
        # Olho direito
        ev3.screen.draw_circle(120, 50, 10, fill=True)

        # Desenhar a boca (arco invertido para parecer triste)
        ev3.screen.draw_arc(90, 100, 30, 180, 360)  # X, Y, raio, ângulo inicial, ângulo final

        # (Opcional) Desenhar sobrancelhas inclinadas para dar expressão triste
        # Sobrancelha esquerda
        ev3.screen.draw_line(50, 30, 70, 40)
        # Sobrancelha direita
        ev3.screen.draw_line(110, 40, 130, 30)


#cor barreiras -> vermelho
#cor linhas -> preto
#cor manteiga -> amarelo
#cor torradeira -> azul 

#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

localizacao = [1,1]     #localização inicial no ambiente
direcao = "frente"
dirCode = 1             #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras
speed = 250             #velocidade inicial
nextDir = ""            #proxima direção
nextDirCode = 0         #código da proxima 

#------------------------------------------------------------------------------------------------------> 
#                           Função pode Andar returna um booleano e recebe uma string com a direção 
#------------------------------------------------------------------------------------------------------> 
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

def temAlgoAqui(): #435 normal
    if distanciaSensor.distance(silent=True) != 435: 
        return True
    else:
        return False

# Função que controla o movimento do robô em uma direção específica

# Função que faz o robo girar à direita e atualiza a direção
def rodar_direita():
    global direcao
    global dirCode
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()
    right_motor.run_angle(1000, 700)
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()
    if direcao == "frente":  # se o robo estava virado para a frente fica virado para a direita
        direcao = "direita"
        dirCode = 3 #sul 
    if direcao == "direita": # se o robo estava virado para a direita fica virado para a trás
        direcao = "atras"
        dirCode = 4 #oeste
    if direcao == "esquerda":
        direcao = "frente"
        dirCode = 2 #este
    if direcao == "atras": # se o robo estava virado para trás fica virado para a esquerda
        direcao = "esquerda"
        dirCode = 1 #norte

 # se o robo estava virado para a frente fica virado para a diesquerda
 # 
 # 
 

#-------------------------------------------------------------------------------------> 
# Função rodar_esquerda 
#------------------------------------------------------------------------------------------------------>
def rodar_esquerda():
    #
    left_motor.run(-speed*2) 
    right_motor.run(-speed*2)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    
    #
    left_motor.run_angle(1000, 700)
    left_motor.run(-speed*2)
    right_motor.run(-speed*2)
    wait(700)

    #para de andar
    left_motor.stop()
    right_motor.stop()

    #atualizar a direcao depois de virar
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
    nextDir=""
    nextDirCode = randint(1,4) # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5 
    #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras 
    if nextDirCode == 2:
        nextDir = "frente"        # norte 
    if nextDirCode == 1:          
        nextDir = "esquerda"      #oeste
    if nextDirCode == 3:
        nextDir == "direita"      #este
    if nextDirCode == 4:
        nextDir == "atras"        #sul
    return nextDir

def andar(nextDir):
    if podeAndar(nextDir):
        if modulo(nextDirCode - dirCode) == 1:
            if nextDir == "esquerda":
                rodar_esquerda()
            else:
                rodar_direita()
        elif modulo(nextDirCode - dirCode) == 2:
            rodar_direita()
            rodar_direita()  # Gira duas vezes para mudar 180°

        left_motor.run(speed/2)
        right_motor.run(speed/2)
        wait(3700)
        if temAlgoAqui() == True:
            colorSensor.color()== Color.RED
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
        elif direcao == "direita":
                localizacao[0] += 1
        elif direcao == "atras":
                localizacao[1] -= 1
        elif direcao == "esquerda":
                localizacao[0] -= 1
        color()
    else:
        ev3.speaker.beep(400, 100)


while True:
    ran = randDir()
    andar(ran)
    