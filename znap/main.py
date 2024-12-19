#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Color, Port  
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, print

from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint, random
import sys
import time


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
toqueSensor = TouchSensor(Port.S3)

#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

localizacao = [1,1]     #localização inicial no ambiente [0] ->linha [0] -> coluna
direcao = "este"        # Diz qual a direçao cardinal que o robô está a apontar
dir_code = 2             #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste
speed = 250             #velocidade inicial
next_dir = ""            #proxima direção (esquerda, direita, frente)
next_dir_code = 0         #código da proxima
#inicialização de variavel para começar o jogo
contador_rondas = 0
localizacao_bolor = [6,6] # localização do bolor inicial
distancia_manteiga = 11 #distancia da manteiga 0 - 10
old_dist = 11 #antiga distancia da manteiga
#info matriz
manteiga = [0,0] 
torradeira = [0,0]

#info adquirida robô
possible_manteiga=[]
found_manteiga=[0,0]
particulas_mas=False
posicoes_torradeira = []
found_torradeira =[0,0]
calor = False
ja_esperou = True
posLegais = []
os_cheiros_anteriores = []
for i in range(6):
    for j in range(6):
        posicoes_torradeira.append([i+1,j+1])

#---------------------------------------------------fim Inicio------------------------------------------> 


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
        print("Manteiga encontrada")
        ev3.screen.clear() # Limpar a tela antes de desenhar
        ev3.screen.draw_text(30, 60, "YAY Manteiga encontrada")
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
        sys.exit()
    else:
        # Limpar a tela antes de desenhar
        ev3.screen.clear()
        ev3.screen.draw_text(10, 20, "A procura da ")
        ev3.screen.draw_text(25, 35, "Manteiga")

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 


#------------------------------------------------------------------------------------------------------> 
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_bolor(encontroMatrix):
    if colorSensor.color() == Color.GREEN or encontroMatrix == True:
        print("Derrotado pelo bolor")
        emoji_triste()
        ev3.screen.draw_text(5, 90, "Derrotado pelo")
        ev3.screen.draw_text(50, 110, "Bolor")
        wait(1000)
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    if colorSensor.color() == Color.BLUE:
        print("Torradeira encontrada")
        #ev3.screen.clear()
        #ev3.screen.draw_text(50, 60, "YAY ta quentinho")
        wait(5000)
    global contador_rondas
    if colorSensor.color() == Color.RED:#Color.RED: 
        ev3.screen.clear()
        ev3.screen.draw_text(5, 60, "YAY ta quentinho")
        contador_rondas+=1
        print("A torradeira está a tostar homem tosta")
        wait(3000)
        return False
    return True    
        #wait(5000)
#----------------------------------------------fim deteta_torradeira----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_barreira deteta as barreiras e tenta evita-las
#------------------------------------------------------------------------------------------------------> 
def deteta_barreira():
    global next_dir_code
    if colorSensor.color()== Color.RED: #se detetar uma barreira
        print("Barreira encontrada")
        left_motor.stop()
        right_motor.stop()
        left_motor.run(-speed/2)
        right_motor.run(-speed/2)
        wait(1850)
        left_motor.stop()
        right_motor.stop()
        #vira para a sul       
        mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
        if not pode_andar():
            if next_dir_code == 1:
                next_dir_code = 3
            elif next_dir_code == 3:
                next_dir_code = 1
        verifica_se_quer_virar() #chama para virar 
        left_motor.run(speed/2)
        right_motor.run(speed/2)
        wait(1850)
    


#---------------------------------------------------fim Deteta_barreira-------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função emoji_triste desenha emogi triste na tela do ev3
#------------------------------------------------------------------------------------------------------>  
'''
def draw_thick_line(x1, y1, x2, y2, thickness):
    for i in range(thickness):
        ev3.screen.draw_line(x1, y1 + i, x2, y2 + i)

def emoji_triste():
        # Limpar a tela antes de desenhar
        ev3.screen.clear()

        # Desenhar os olhos (círculos)
        # Olho esquerdo
        ev3.screen.draw_circle(60, 50, 10, fill=True)
        # Olho direito
        ev3.screen.draw_circle(120, 50, 10, fill=True)

        # Desenhar a boca (linha reta para parecer triste)
        draw_thick_line(70, 80, 110, 80, 3)  # X1, Y1, X2, Y2, espessura

        # (Opcional) Desenhar sobrancelhas inclinadas para dar expressão triste
        # Sobrancelha norte
        ev3.screen.draw_line(50, 30, 70, 40)
        # Sobrancelha sul
        ev3.screen.draw_line(110, 40, 130, 30)
'''
#---------------------------------------------------fim emoji_triste----------------------------------> 



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
#                           Funç es que controlam o movimento do robô em direç es espec ficas
#------------------------------------------------------------------------------------------------------>

#------------------------------------------------------------------------------------------------------>
#                                   Funç o que preparar o robo para poder girar
#------------------------------------------------------------------------------------------------------>
def prepara_rodar():
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
    right_motor.run_angle(1000, -600) # 1 velocidade 2 angulo
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()
    dir_code = (dir_code % 4) + 1
    if direcao == "este":  # se o robo estava virado para a este fica virado para a sul
        direcao = "sul"
    elif direcao == "sul": # se o robo estava virado para a sul fica virado para a trás
        direcao = "oeste"
    elif direcao == "norte":
        direcao = "este"
    elif direcao == "oeste": # se o robo estava virado para trás fica virado para a norte
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
    left_motor.run_angle(1000, -600)  # 1 velocidade 2 angulo
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
    elif direcao == "norte":
        direcao = "oeste"
    elif direcao == "oeste":
        direcao = "sul"
    elif direcao == "sul":
        direcao = "este"

#---------------------------------------------------fim rodar_esquerda--------------------------------->

#------------------------------------------------------------------------------------------------------> 
# Função rand_dir retorna a próxima direção a se movimentar aleatoriamente
#------------------------------------------------------------------------------------------------------>
def rand_dir():
    global next_dir #direção a seguir
    global next_dir_code #codigo da direção a seguir
    next_dir_code = randint(1,3) # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5
    #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste
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
        next_dir = "esquerda"
    elif next_dir_code == 2:
        next_dir = "frente"
    elif next_dir_code == 3:
        next_dir = "direita"
        

#---------------------------------------------------fim randDir------------------------------------------>

#------------------------------------------------------------------------------------------------------> 
# Função mini_rand retorna a próxima direção a se movimentar aleatoriamente
#------------------------------------------------------------------------------------------------------>
def mini_rand_dir():
    global next_dir #direção a seguir
    global next_dir_code #codigo da direção a seguir
    esq_dir = randint(1,2) # guarda um número aletório de 0 a 4 + 1 ou seja, de 1 a 5
    #codigo da direção atual, 1=norte, 2=este, 3=sul e 4=oeste
    if esq_dir == 1: #se calhar 1 vira para a esquerda
        next_dir_code = 1   
        next_dir = "esquerda"
    elif esq_dir == 2: #se calhar 2 vira para a direita
        next_dir_code = 3
        next_dir = "direita"
        

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
    if next_dir_code != 2: #tem de virar mas não precisa de fazer 180
        if next_dir_code == 1:
            rodar_esquerda()
            print("Vira para a esquerda: code -> " + str(dir_code) + " direção -> " + direcao)
        else:
            rodar_direita()
            print("Vira para a direita: code -> " + str(dir_code) + " direção -> " + direcao)

#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç o selecionada, ir  andar nessa direç o e atualizar a sua posiç o
#-------------------------------------------------------------------------------------------------------->
def andar():
    print("Direção atual:  " + direcao + " code -> " + str(dir_code))
    verifica_se_quer_virar()
    #anda
    left_motor.run(speed/2)
    right_motor.run(speed/2)
    wait(3000)

    deteta_barreira()
    wait(4500)
    wait(1850)

    deteta_barreira()
    
    wait(5650)
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
# Função que atualiza a localização do robô
#-------------------------------------------------------------------------------------------------------->
def mostrar_localizacao(localizacao):
    # Obter as coordenadas x e y da posição, ajustando para índice zero
    x, y = localizacao[0] - 1, localizacao[1] - 1
    xb, yb = localizacao_bolor[0] - 1, localizacao_bolor[1] - 1
    # Verificar se as coordenadas estão dentro dos limites da matriz
    if not (0 <= x < 6 and 0 <= y < 6):
        print("Posição fora dos limites da matriz.")
        return

    # Construir a matriz com bordas
    for i in range(6):
        # Linha superior das células
        print(" _   " * 6)
        
        # Linha com conteúdo das células
        linha = ""
        for j in range(6):
            if i == x and j == y:
                linha += "| X "  # Marca a posição especificada com 'X'
            elif i == xb and j == yb:
                linha += "| B "  # Marca a posição especificada com B
            else:
                linha += "|   "  # Célula vazia
        linha += "|"  # Final da linha
        print(linha)
    if x == xb and y == yb:
        deteta_bolor(True)
    # Linha inferior das células
    print(" _   " * 6)


#-------------------------------------------------------------------------------------------------------->
# Funções para calibrar sensor de cor
#-------------------------------------------------------------------------------------------------------->
def calibra_color_sensor(sensor):
    ev3.speaker.beep()  # Som para indicar o início da calibração
    print("Coloque o sensor sobre uma superfície preta e pressione o botão central.")
    
    # Espera até que o botão central seja pressionado para calibrar o preto
    while not any(ev3.buttons.pressed()):
        wait(10)
    preto = sensor.reflection()
    print("Reflexão no preto:", preto)
    wait(1000)  # Tempo para ajustar a posição
    ev3.speaker.beep()  # Som para indicar o início da calibração
    print("Coloque o sensor sobre uma superfície branca e pressione o botão central.")
    
    # Espera até que o botão central seja pressionado para calibrar o branco
    while not any(ev3.buttons.pressed()):
        wait(10)
    branco = sensor.reflection()
    print("Reflexão no branco:", branco)
    
    # Calcula a faixa de calibração
    if branco - preto == 0:
        raise ValueError("Erro na calibração: reflexões preta e branca são iguais.")
    
    return preto, branco

def get_reflexao_calibrada(sensor, preto, branco):
    # Obtenção e normalização da leitura atual do sensor
    reflexão = sensor.reflection()
    calibra_reflexão = (reflexão - preto) / (branco - preto) * 100
    return max(0, min(100, calibra_reflexão))  # Limita a faixa de 0 a 100




#-------------------------------------------------------------------------------------------------------->
# Função que representa o cheiro do bolor
#-------------------------------------------------------------------------------------------------------->
#def cheiro_bolor():
    # N - S - E - O
    # se encontrar 1 a manteiga acaba o jogo como representar? 
    #localização incial = [6,6]
    #pode saltar barreiras 
    #[6,6] -> [5,6] -> ?
    #localizacao_bolor

#-------------------------------------------------------------------------------------------------------->
# Função que deteta a cor e associa ao cheiro de um dos elementos
#-------------------------------------------------------------------------------------------------------->
def cheirar():
    global next_dir_code
    print("Cheirando")
    ev3.screen.clear() # Limpar a tela antes de desenhar
    ev3.screen.draw_text(5, 90, "Cheirando")
    while True:
        #verde -> bom caminho
        #castanho -> caminho mau 
        #if toqueSensor.pressed():
        if colorSensor.color() == Color.WHITE: #sentir calor 
            print("Torradeira está perto") # 1 casa
            ev3.screen.clear() # Limpar a tela antes de desenhar
            ev3.screen.draw_text(5, 90, "Torradeira está perto")
            wait(2000)
        if colorSensor.color() == Color.GREEN:
            print("Caminho mais perto da manteiga")
            next_dir_code = 2
            if ((localizacao[1] == 6 and dir_code == 2) or (localizacao[0] == 6 and dir_code == 3) or 
                (localizacao[1] == 1 and dir_code == 4) or (localizacao[0] == 1 and dir_code == 1)):
                print("Não posso andar")
                mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
                if not pode_andar():
                    print("mini errado")
                    if next_dir_code == 1:
                        next_dir_code = 3
                    elif next_dir_code == 3:
                        next_dir_code = 1
            ev3.screen.clear() # Limpar a tela antes de desenhar            
            return False
        elif colorSensor.color() == Color.BROWN: #Color.RED
            print("Caminho mais longe da manteiga")
            ev3.screen.clear() # Limpar a tela antes de desenhar
            return True
            
# Código para a matriz do bolor
def bolor_calculator():
    global localizacao_bolor
    caminhos = {
        "norte" : modulo((localizacao[0] - (localizacao_bolor[0] - 1))) + modulo((localizacao[1] - localizacao_bolor[1])), 
        "sul" : modulo((localizacao[0] - (localizacao_bolor[0] + 1))) + modulo((localizacao[1] - localizacao_bolor[1])),
        "este" : modulo((localizacao[1] - (localizacao_bolor[1] + 1))) + modulo((localizacao[0] - localizacao_bolor[0])),
        "oeste" : modulo((localizacao[1] - (localizacao_bolor[1] - 1))) + modulo((localizacao[0] - localizacao_bolor[0]))
    }
    #print("norte bolor: " + str(caminhos["norte"]))
    #print("sul bolor: " + str(caminhos["sul"]))
    #print("este bolor: " + str(caminhos["este"]))
    #print("oeste bolor: " + str(caminhos["oeste"]))
    min_local = 999 #menor distancia ao bolor
    if caminhos["norte"] < min_local:
        min_local = caminhos["norte"] #4
    if caminhos["sul"] < min_local:  #6
        min_local = caminhos["sul"] #4
    if caminhos["este"] < min_local: #6
        min_local = caminhos["este"] #4
    if caminhos["oeste"] < min_local: #4
        min_local = caminhos["oeste"] #4
    print("caminho mais proximo para o bolor: " + str(min_local))
    if min_local <= 2:
        print("A " + str(min_local) + " casas do bolor")
    if caminhos["norte"] == min_local:
        localizacao_bolor[0] -= 1
        print ("bolor foi para norte")
        print("bolor tá em " + str(localizacao_bolor))
        return 0
    elif caminhos["sul"] == min_local:
        localizacao_bolor[0] += 1
        print("bolor foi para sul")
        print("bolor tá em " + str(localizacao_bolor))
        return 0
    elif caminhos["este"] == min_local:
        localizacao_bolor[1] += 1
        print("bolor foi para este")
        print("Localizacao do bolor: " + str(localizacao_bolor))
        return 0
    elif caminhos["oeste"] == min_local:
        localizacao_bolor[1] -= 1
        print("bolor foi para oeste")
        print("Localizacao do bolor: " + str(localizacao_bolor))
        return 0
        
def dist_manteiga():
    global next_dir_code
    global distancia_manteiga
    global old_dist #distancia anterior
    print("Cheirando")
    ev3.screen.clear() # Limpar a tela antes de desenhar
    ev3.screen.draw_text(5, 90, "Cheirando")
    #deteta_manteiga()
    while True:
        if toqueSensor.pressed() == False:
            if colorSensor.color() == Color.GREEN:
                distancia_manteiga = 1
                break
            elif colorSensor.color() == Color.YELLOW:
                distancia_manteiga = 2
                break
            elif colorSensor.color() == Color.RED:
                distancia_manteiga = 3  
                break
        elif toqueSensor.pressed() == True:
            if colorSensor.color() == Color.GREEN:
                distancia_manteiga = 4
                break
            elif colorSensor.color() == Color.YELLOW:
                distancia_manteiga = 5
                break
            elif colorSensor.color() == Color.RED:
                distancia_manteiga = 6
                break
        if colorSensor.color() == Color.WHITE:  
            print("Torradeira está perto") # 1 casa
            wait(2000)

    compara_dist()

def compara_dist():
    global next_dir_code
    global old_dist
    print("Distancia anteriror da manteiga: " + str(old_dist))
    if old_dist < distancia_manteiga:
        old_dist = distancia_manteiga
        print("Caminho mais longe da manteiga")
        print("Distancia atual da manteiga: " + str(distancia_manteiga))
        ev3.screen.clear() # Limpar a tela antes de desenhar
        print("Casas de distância da manteiga: " + str(distancia_manteiga))
        retry = True
        while retry:       
            mini_rand_dir()
            if pode_andar():
                retry = False
    elif old_dist >= distancia_manteiga:
        old_dist = distancia_manteiga
        print("Caminho mais perto da manteiga")
        print("Distancia da manteiga: " + str(distancia_manteiga))
        next_dir_code = 2
        if ((localizacao[1] == 6 and dir_code == 2) or (localizacao[0] == 6 and dir_code == 3) or 
            (localizacao[1] == 1 and dir_code == 4) or (localizacao[0] == 1 and dir_code == 1)):
            print("Não posso andar")
            mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
            if not pode_andar():
                print("mini errado")
                if next_dir_code == 1:
                    next_dir_code = 3
                elif next_dir_code == 3:
                    next_dir_code = 1
        ev3.screen.clear() # Limpar a tela antes de desenhar            
'''
    elif old_dist == distancia_manteiga:
        retryD = True
        while retryD:
            
            if ((localizacao[1] == 6 and dir_code == 2) or (localizacao[0] == 6 and dir_code == 3) or 
            (localizacao[1] == 1 and dir_code == 4) or (localizacao[0] == 1 and dir_code == 1)):
                retry = False'''

    
    
    
    

#-------------------------------------------------------------------------------------------------------->
# Ciclo de teste de código
#-------------------------------------------------------------------------------------------------------->

#Calibração
preto, branco = calibra_color_sensor(colorSensor)
ev3.speaker.beep()  # Som para indicar o fim da calibração
wait(1000)
ev3.speaker.beep()  # Som para indicar o fim da calibração
print("Calibração concluída.")

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

    print("************* Ronda: " + str(contador_rondas) + " *************")
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, "A procura da ")
    ev3.screen.draw_text(25, 35, "Torradeira")
    if deteta_torradeira():
        retry = True
        wait(1000)
        if contador_rondas == 0:
            while retry:        
                rand_dir()          # decidir uma direção aleatória
                if pode_andar():
                    retry = False
        else:
            dist_manteiga()
               
        #print("nao saio daqui")
        #print(pode_andar())
        while pode_andar():
            andar()
            break             # movimenta-se para a direção
        if deteta_manteiga():
            break
        if deteta_bolor(False):
            break
        print("Localizacao atual do robo: " + str(localizacao))  # imprimi a localização atual
    bolor_calculator()
    mostrar_localizacao(localizacao)
    wait(3000)  # espera pela proxima ronda
    contador_rondas += 1
    ev3.speaker.beep(400, 100)
    ev3.screen.clear()
    print("----------------------------------------------------------------->")