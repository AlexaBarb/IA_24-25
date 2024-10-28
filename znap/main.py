#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, UltrasonicSensor,ColorSensor, Screen
from pybricks.parameters import Port, Direction,Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint
import sys


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

#inicialização de variavel para começar o jogo
novo_jogo = True

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_manteaiga_bolor deteta  manteiga e agarra-a, ou se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_manteiga_bolor():
    if colorSensor.color() == Color.YELLOW:
        
        ev3.screen.clear() # Limpar a tela antes de desenhar
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
    # elif colorSensor.color() == Color.GREEN:
    #     emoji_triste()
    #     sys.exit()
    else:
        # Limpar a tela antes de desenhar
        ev3.screen.clear()
        ev3.screen.draw_text(50, 60, "A procura da Manteiga")

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_bolor():
    if colorSensor.color() == Color.GREEN:
        emoji_triste()
        ev3.screen.draw_text(50, 60, "Derrotado pelo Bolor")
        wait(1000)
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    if colorSensor.color() == Color.BLUE:
        ev3.screen.clear()
        ev3.screen.draw_text(50, 60, "YAY ta quentinho")
        wait(5000)
#----------------------------------------------fim deteta_torradeira----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_barreira deteta as barreiras e tenta evita-las
#------------------------------------------------------------------------------------------------------> 
def deteta_barreira():
    if tem_algo_aqui(): #chama função que verfica se tem algo em frente do robô
            if colorSensor.color()== Color.RED: #se detetar uma barreira 
                ev3.screen.clear()
                emoji_triste()#mostrar cara triste no ecrã
                ev3.screen.draw_text(10, 120, "A procura da Manteiga")
                #para e move-se para a frente para conseguir virar
                left_motor.stop()
                right_motor.stop()
                left_motor.run(-speed/2)
                right_motor.run(-speed/2)
                wait(1850)
                left_motor.stop()
                right_motor.stop()
                #vira para a direita 
                rodar_direita()
#---------------------------------------------------fim Deteta_barreira-------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função emoji_triste desenha emogi triste na tela do ev3
#------------------------------------------------------------------------------------------------------>  

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

#---------------------------------------------------fim emoji_triste----------------------------------> 


#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

#def Inicio():
localizacao = [1,1]     #localização inicial no ambiente [0] ->linha [0] -> coluna
direcao = "frente"
dir_code = 2             #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras
speed = 250             #velocidade inicial
next_dir = ""            #proxima direção
next_dir_code = 0         #código da proxima
#---------------------------------------------------fim Inicio------------------------------------------> 

#------------------------------------------------------Nota--------------------------------------------->
#cor barreiras -> vermelho
#cor bolor -> verde
#cor manteiga -> amarelo
#cor torradeira -> azul 
#---------------------------------------------------fim nota-------------------------------------------->

#------------------------------------------------------------------------------------------------------> 
# Função pode_andar retorna um booleano usa uma string direção para testar se pode andar
#------------------------------------------------------------------------------------------------------> 
def pode_andar(): #função que verifica se é possível andar na direção indicada
    if localizacao[1] == 1 and next_dir == "esquerda": #se encontra-se no 1 quadrado/primeira linha e testa para a esquerda
        return False #fora dos limites do ambiente
    elif localizacao[1] == 6 and next_dir == "frente": #se encontra-se no 6 quadrado/ ultima coluna e testa para a frente  
        return False
    elif localizacao[0] == 6 and next_dir == "direita": #se encontra-se no 6 quadrado/ultima linha e testa para a direita
        return False
    elif localizacao[0] == 1 and next_dir == "atras": #se encontra-se no 1 quadrado/ primeira coluna e testa para atrás 
        return False
    else:
        return True
#---------------------------------------------------fim pode_andar------------------------------------>

#-------------------------------------------------------------------------------------------------------->
#   Função modulo recebe um valor e retorna o valor absoluto 
#-------------------------------------------------------------------------------------------------------->
def modulo(a):
    if a < 0:
        return -a
    else:
        return a
#---------------------------------------------------fim modulo------------------------------------------>

#------------------------------------------------------------------------------------------------------>
# Função tem_algo_aqui retorna um booleano e verifica se há algo a frente
#------------------------------------------------------------------------------------------------------>
def tem_algo_aqui(): #435 normal
    if distanciaSensor.distance(silent=True) != 435:  #se o sensor de distância detetar algo
        return True
    else:
        return False
#---------------------------------------------------fim temAlgoAqui------------------------------------>

#------------------------------------------------------------------------------------------------------>
#                           Funç�es que controlam o movimento do robô em direç�es espec�ficas
#------------------------------------------------------------------------------------------------------>

#------------------------------------------------------------------------------------------------------>
#                                   Funç�o que preparar o robo para poder girar
#------------------------------------------------------------------------------------------------------>
def prepara_rodar():
    global direcao
    global dir_code
    left_motor.run(speed*3)
    right_motor.run(speed*3)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()

#---------------------------------------------------fim prepara_rodar----------------------------------->

#------------------------------------------------------------------------------------------------------>
# Função rodar_direita que faz o robo girar à direita e atualiza a direção
#------------------------------------------------------------------------------------------------------>
def rodar_direita():
    global direcao
    global dir_code
    prepara_rodar()
    right_motor.run_angle(1000, -700)
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()
    if direcao == "frente":  # se o robo estava virado para a frente fica virado para a direita
        direcao = "direita"
        dir_code = 3 #sul
    if direcao == "direita": # se o robo estava virado para a direita fica virado para a trás
        direcao = "atras"
        dir_code = 4 #oeste
    if direcao == "esquerda":
        direcao = "frente"
        dir_code = 2 #este
    if direcao == "atras": # se o robo estava virado para trás fica virado para a esquerda
        direcao = "esquerda"
        dir_code = 1 #norte

 # se o robo estava virado para a frente fica virado para a esquerda

 #---------------------------------------------------fim rodar_direita----------------------------------->
 
 
#--------------------------------------------------------------------------------------------------------> 
# Função rodar_esquerda 
#-------------------------------------------------------------------------------------------------------->
def rodar_esquerda():
    global direcao
    global dir_code
    prepara_rodar()
    left_motor.run_angle(1000, -700)
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700)

    #para de andar
    left_motor.stop()
    right_motor.stop()

    #atualizar a direcao depois de virar
    if direcao == "frente":
        direcao = "esquerda"
        dir_code = 1
    if direcao == "esquerda":
        direcao = "atras"
        dir_code = 4
    if direcao == "atras":
        direcao = "direita"
        dir_code = 3
    if direcao == "direita":
        direcao = "frente"
        dir_code = 2

#---------------------------------------------------fim rodar_esquerda--------------------------------->

#------------------------------------------------------------------------------------------------------> 
# Função rand_dir retorna a próxima direção a se movimentar aleatoriamente
#------------------------------------------------------------------------------------------------------>
def rand_dir():
    global next_dir
    global next_dir_code
    next_dir_code = randint(1,4) # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5
    #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras 
    if next_dir_code == 2:
        next_dir = "frente"        # norte
    if next_dir_code == 1:
        next_dir = "esquerda"      #oeste
    if next_dir_code == 3:
        next_dir = "direita"      #este
    if next_dir_code == 4:
        next_dir = "atras"        #sul
    print(direcao)
    print(next_dir)


#---------------------------------------------------fim randDir------------------------------------------>

#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç�o selecionada, ir� andar nessa direç�o e atualizar a sua posiç�o
#-------------------------------------------------------------------------------------------------------->
def andar():
    if pode_andar():
        if modulo(next_dir_code - dir_code) == 1:
            if next_dir == "esquerda":
                rodar_esquerda()
            else:
                rodar_direita()
        elif modulo(next_dir_code - dir_code) == 2:
            rodar_direita()
            rodar_direita()  # Gira duas vezes para mudar 180°
        left_motor.run(speed/2)
        right_motor.run(speed/2)
        wait(3700)
        #if tem_algo_aqui():
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
        if dir_code == 2:
                localizacao[0] += 1
        elif dir_code == 3:
                localizacao[1] += 1
        elif dir_code == 1:
                localizacao[1] -= 1
        elif dir_code == 4:
                localizacao[0] -= 1
        deteta_manteiga_bolor()
    else:
        ev3.speaker.beep(400, 100)
#---------------------------------------------------fim andar--------------------------------------------->

#-------------------------------------------------------------------------------------------------------->
# Ciclo de teste de código
#-------------------------------------------------------------------------------------------------------->
while True:
    print(localizacao)
    rand_dir()
    andar()
    wait(2000)

# while True:
    
#     if novo_jogo == True:
#         localizacao = [1,1]     #localização inicial no ambiente [0] ->linha [0] -> coluna
#         direcao = "frente"
#         dir_code = 2             #codigo da direção atual, 1=esquerda, 2=frente, 3=direita e 4=atras
#         speed = 250             #velocidade inicial
#         next_dir = ""            #proxima direção
#         next_dir_code = 0         #código da proxima
        
   
#         pode_andar(direcao)

#         deteta_agarra_manteiga()

#         rand_dir()

#         pode_andar(direcao)
        
#         #rodar_direita()
#         #rodar_esquerda()
#         #andar(next_dir)
        
#         #tem_algo_aqui()
#         #ran = rand_dir()
#         #andar(ran)
        
#     if game_over == True
#     novo_jogo = True
    
#nota: falta ver barreira/torradeira/bolor como escrevemos no código
