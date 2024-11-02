#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
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
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------>
def deteta_bolor():
    if colorSensor.color() == Color.GREEN:
        #emoji_triste()
        #ev3.screen.draw_text(50, 60, "Derrotado pelo Bolor")
        wait(1000)
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_manteaiga_bolor deteta  manteiga e agarra-a, ou se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_manteiga():
    if colorSensor.color() == Color.YELLOW:
        #ev3.screen.clear() # Limpar a tela antes de desenhar
        #ev3.screen.draw_text(50, 60, "YAY Manteiga encontrada")
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
        wait(3800)
        left_motor.stop()
        right_motor.stop()
        print("Manteiga encontrada")
        return True
    else:
        # Limpar a tela antes de desenhar
        #ev3.screen.clear()
        #ev3.screen.draw_text(50, 60, "A procura da Manteiga")
        print("A procura da Manteiga")
        return False

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 


#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    if colorSensor.color() == Color.BLUE:
        print("Torradeira encontrada")
        #ev3.screen.clear()
        #ev3.screen.draw_text(50, 60, "YAY ta quentinho")
        wait(5000)
#----------------------------------------------fim deteta_torradeira----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_barreira deteta as barreiras e tenta evita-las
#------------------------------------------------------------------------------------------------------> 
def deteta_barreira():
    global direcao
    #if tem_algo_aqui(): #chama função que verfica se tem algo em este do robô
    if colorSensor.color()== Color.RED: #se detetar uma barreira
        print("Barreira encontrada")
        #ev3.screen.clear()
        #emoji_triste()#mostrar cara triste no ecrã
        #ev3.screen.draw_text(10, 120, "A procura da Manteiga")
        #para e move-se para a este para conseguir virar
        left_motor.stop()
        right_motor.stop()
        left_motor.run(-speed/2)
        right_motor.run(-speed/2)
        wait(1850)
        left_motor.stop()
        right_motor.stop()
        #vira para a sul
        rodar_direita()
        print("Direção a mudar:" + direcao)
        left_motor.run(speed/2)
        right_motor.run(speed/2)
        wait(4500)
        left_motor.stop()
        right_motor.stop()



#---------------------------------------------------fim Deteta_barreira-------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função emoji_triste desenha emogi triste na tela do ev3
#------------------------------------------------------------------------------------------------------>  
'''
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
        # Sobrancelha norte
        ev3.screen.draw_line(50, 30, 70, 40)
        # Sobrancelha sul
        ev3.screen.draw_line(110, 40, 130, 30)
'''
#---------------------------------------------------fim emoji_triste----------------------------------> 


#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

#def Inicio():
localizacao = [1,1]     #localização inicial no ambiente [0] ->linha [0] -> coluna
direcao = "este"
dir_code = 2             #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste
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
    if localizacao[0] <= 1 and next_dir_code == 1: #se encontra-se no 1 quadrado/primeira linha e testa para a norte
        return False #fora dos limites do ambiente
    elif localizacao[1] >= 6 and next_dir_code == 2: #se encontra-se no 6 quadrado/ ultima coluna e testa para a este
        return False
    elif localizacao[0] >= 6 and next_dir_code == 3: #se encontra-se no 6 quadrado/ultima linha e testa para a sul
        return False
    elif localizacao[1] <= 1 and next_dir_code == 4: #se encontra-se no 1 quadrado/ primeira coluna e testa para atrás
        return False
    elif modulo(next_dir_code - dir_code) == 2:
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
# Função tem_algo_aqui retorna um booleano e verifica se há algo a este
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
# Função rodar_direita que faz o robo girar à sul e atualiza a direção
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
    dir_code = (dir_code % 4) + 1
    if direcao == "este":  # se o robo estava virado para a este fica virado para a sul
        direcao = "sul"
    if direcao == "sul": # se o robo estava virado para a sul fica virado para a trás
        direcao = "oeste"
    if direcao == "oeste": # se o robo estava virado para trás fica virado para a norte
        direcao = "norte"
    if direcao == "norte":
        direcao = "este"


 # se o robo estava virado para a este fica virado para a norte

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

    dir_code = (dir_code - 2) % 4 + 1
    #atualizar a direcao depois de virar
    if direcao == "este":
        direcao = "norte"
    if direcao == "norte":
        direcao = "oeste"
    if direcao == "oeste":
        direcao = "sul"
    if direcao == "sul":
        direcao = "este"

#---------------------------------------------------fim rodar_esquerda--------------------------------->

#------------------------------------------------------------------------------------------------------> 
# Função rand_dir retorna a próxima direção a se movimentar aleatoriamente
#------------------------------------------------------------------------------------------------------>
def rand_dir():
    global next_dir #direção a seguir
    global next_dir_code #codigo da direção a seguir
    next_dir_code = randint(1,4) # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5
    #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste 
    if next_dir_code == 2:
        next_dir = "este"        # norte
    if next_dir_code == 1:
        next_dir = "norte"      #oeste
    if next_dir_code == 3:
        next_dir = "sul"      #este
    if next_dir_code == 4:
        next_dir = "oeste"        #sul
    #print("Direção atual:" + direcao) #atual                   --------------------------ver melhor pk n muda!!!!!!!!!!!!!!!!!!!!!
    print("Próxima direção: " + next_dir +
          " | Direções atual: " + str(dir_code) +
          " | Direções seguinte: " + str(next_dir_code)) #proxima direção


#---------------------------------------------------fim randDir------------------------------------------>

def verifica_se_quer_virar():
   # global direcao
    if modulo(next_dir_code - dir_code) == 1: #tem de virar mas não precisa de fazer 180
        if next_dir_code - dir_code == -1:
            rodar_esquerda()
            #print("Vira para a esquerda:" + direcao)
        else:
            rodar_direita()
            #print("Vira para a direita:" + direcao)

def verifica_se_quer_rodar():
    if modulo(next_dir_code - dir_code) == 2:
        print(direcao)
        rodar_direita()
        print(direcao)
        rodar_direita()  # Gira duas vezes para mudar 180°
        print(direcao)
#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç�o selecionada, ir� andar nessa direç�o e atualizar a sua posiç�o
#-------------------------------------------------------------------------------------------------------->
def andar():
    verifica_se_quer_virar()
    verifica_se_quer_rodar()
    #anda
    left_motor.run(speed/2)
    right_motor.run(speed/2)
    wait(3000)

    deteta_barreira()
    wait(4500)
    left_motor.stop()
    right_motor.stop()
    mudaLocalizacao()
#---------------------------------------------------fim andar--------------------------------------------->


#-------------------------------------------------------------------------------------------------------->
# Função que atualiza a localização do robô
#-------------------------------------------------------------------------------------------------------->
def mudaLocalizacao():
    global localizacao
    if dir_code == 2: #este
            localizacao[1] += 1 # aumenta na coluna
    elif dir_code == 3: #sul
            localizacao[0] += 1 #retira na linha
    elif dir_code == 1: #norte
            localizacao[0] -= 1 #aumenta na linha
    elif dir_code == 4: #oeste
            localizacao[1] -= 1 #tira da coluna

def arranjaDir():
    global dir_code
    if direcao == "este":
        dir_code = 2
    if direcao == "norte":
        dir_code = 1
    if direcao == "oeste":
        dir_code = 4
    if direcao == "sul":
        dir_code = 3


#-------------------------------------------------------------------------------------------------------->
# Ciclo de teste de código
#-------------------------------------------------------------------------------------------------------->
while True:
    print(localizacao)  # imprimi a localização atual
    rand_dir()          # decidir uma direção aleatória
    if pode_andar():
        '''
        dir_code = next_dir_code
        direcao = next_dir
        mudaLocalizacao()  # atualiza a localização
        '''
        andar()             # movimenta-se para a direção
        if deteta_bolor():
            break
        if deteta_manteiga():
            break
        deteta_torradeira()
        wait(2000)  # espera pela proxima ronda
    else:
        print("Direção Inválida")

# while True:
    
#     if novo_jogo == True:
#         localizacao = [1,1]     #localização inicial no ambiente [0] ->linha [0] -> coluna
#         direcao = "este"
#         dir_code = 2             #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste
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
