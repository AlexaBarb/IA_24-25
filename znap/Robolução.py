#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from random import randint, random
import sys
import time

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Direction, Color, Port  
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, print

from pybricks.media.ev3dev import SoundFile, ImageFile


#------------------------------------------------------------------------------------------------------> 
#                                       inicializações 
#------------------------------------------------------------------------------------------------------>
#criação de uma instancia do módulo principal 
ev3= EV3Brick()
music = SoundFile()
#inicialização dos motores
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.D)

#inicialização do sensor de cor
colorSensor = ColorSensor(Port.S2)
#distanciaSensor = UltrasonicSensor(Port.S1)
toqueSensor = TouchSensor(Port.S3)


#------------------------------------------------------------------------------------------------------> 
#                                       Movimento Inicial 
#------------------------------------------------------------------------------------------------------> 

#def Inicio():
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
barreiras = []
barreiras_fixas_ao_descer = [[2, 3], [3, 4], [4, 3], [5, 5]]
barreiras_fixas_a_direita = [[2, 5]]
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
#       Função deteta_manteaiga_bolor deteta  manteiga e agarra-a, ou se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_manteiga():
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, "A procura da ")
    ev3.screen.draw_text(25, 35, "Manteiga")
    print("A procura da Manteiga")
    if colorSensor.color() == Color.YELLOW:
        print("O robô esta: " + str(localizacao))
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
        ev3.screen.clear() # Limpar a tela antes de desenhar
        ev3.screen.draw_text(30, 60, "YAY Manteiga encontrada")
        sys.exit()
    elif colorSensor.color() == Color.GREEN:
        print("Derrotado pelo bolor")
        sys.exit()
    

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_bolor(aux):
    if colorSensor.color() == Color.GREEN or aux == True:
        print("Derrotado pelo bolor")
        emoji_triste()
        ev3.screen.draw_text(5, 90, "Derrotado pelo")
        ev3.screen.draw_text(50, 110, "Bolor")
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    global contador_rondas
    global found_torradeira
    global ja_esperou
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, "A procura da ")
    ev3.screen.draw_text(25, 35, "Torradeira")
    # conta_torradas = 0
    # while conta_torradas <10 :
    if colorSensor.color() == Color.WHITE and ja_esperou:

        ev3.speaker.beep(400, 100) 
        wait(500)
        ja_esperou = False
        found_torradeira = localizacao
        ev3.screen.clear()
        ev3.screen.draw_text(5, 60, "YAY ta quentinho")
        print("A torradeira está a tostar homem tosta")
        #print("ja_esperou:" + str(ja_esperou))
        ev3.speaker.beep(400, 100) 
        wait(500)
        return False
    ja_esperou = True
    #print("ja_esperou:" + str(ja_esperou))
    return True    
        
#----------------------------------------------fim deteta_torradeira----------------------------------->

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

#------------------------------------------------------------------------------------------------------> 
# Função pode_andar retorna um booleano usa uma string direção para testar se pode andar
#------------------------------------------------------------------------------------------------------> 
def pode_andar(): #função que verifica se é possível andar na direção indicada
    global posLegais
    if localizacao[0] <= 1: #se encontra-se no 1 quadrado/primeira linha e testa para a norte
        if dir_code == 2 and next_dir_code == 1:
            return False
        if dir_code == 4 and next_dir_code == 3:
            return False
        if dir_code == 1 and next_dir_code == 2:
            return False  
    elif localizacao[1] >= 6: #se encontra-se no 6 quadrado/ ultima coluna e testa para a este
        if dir_code == 2 and next_dir_code == 2:
            return False
        if dir_code == 3 and next_dir_code == 1:
            return False
        if dir_code == 1 and next_dir_code == 3:
            return False
    elif localizacao[0] >= 6: #se encontra-se no 6 quadrado/ultima linha e testa para a sul
        if dir_code == 3 and next_dir_code == 2:
            return False
        if dir_code == 2 and next_dir_code == 3:
            return False
        if dir_code == 1 and next_dir_code == 1:
            return False
    elif localizacao[1] <= 1: #se encontra-se no 1 quadrado/ primeira coluna e testa para atrás
        if dir_code == 3 and next_dir_code == 3:
            return False
        if dir_code == 1 and next_dir_code == 1:
            return False
        if dir_code == 4 and next_dir_code == 2:
            return False  
    return True
#---------------------------------------------------fim pode_andar------------------------------------>


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

#---------------------------------------------------fim emoji_triste----------------------------------> 



#-------------------------------------------------------------------------------------------------------->
#   Função abs recebe um valor e retorna o valor absoluto 
#-------------------------------------------------------------------------------------------------------->

#---------------------------------------------------fim abs------------------------------------------>
def prepara_rodar():
    left_motor.run(speed*3)
    right_motor.run(speed*3)
    wait(700) # Espera 700 ms
    left_motor.stop()
    right_motor.stop()


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
        next_dir = "esquerda"
    elif next_dir_code == 2:
        next_dir = "frente"
    elif next_dir_code == 3:
        next_dir = "direita"
        

#---------------------------------------------------fim randDir------------------------------------------>


def verifica_se_quer_virar():
    if next_dir_code != 2: #tem de virar mas não precisa de fazer 180
        if next_dir_code == 1:
            rodar_esquerda()
            print("Vira para a esquerda: code -> " + str(dir_code) + " direção -> " + direcao)
        elif next_dir_code == 3:
            rodar_direita()
            print("Vira para a direita: code -> " + str(dir_code) + " direção -> " + direcao)
        else:
            rodar_direita()
            rodar_direita()
            print("Dá um 180º: code ->" + str(dir_code) + " direção -> " + direcao)
            

#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç o selecionada, ir  andar nessa direç o e atualizar a sua posiç o
#-------------------------------------------------------------------------------------------------------->
def andar():
    print("Direção robô:  " + direcao + " code -> " + str(dir_code))
    verifica_se_quer_virar()
    left_motor.run(speed/2)
    right_motor.run(speed/2)
    wait(3000)

    deteta_barreira()
    wait(4500)
    #wait(1850)
    
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

#-------------------------------------------------------------------------------------------------------->
# Função que atualiza a localização do robô
#-------------------------------------------------------------------------------------------------------->


def mostrar_localizacao(localizacao, found_manteiga, found_torradeira):
    # Obter as coordenadas x e y da posição, ajustando para índice zero
    x, y = localizacao[0] - 1, localizacao[1] - 1
    xb, yb = localizacao_bolor[0] - 1, localizacao_bolor[1] - 1
    xm, ym = found_manteiga[0] - 1, found_manteiga[1] - 1
    xt, yt = found_torradeira[0] - 1, found_torradeira[1] - 1
    # Verificar se as coordenadas estão dentro dos limites da matriz
    if not (0 <= x < 6 and 0 <= y < 6):
        print("Posição fora dos limites da matriz.")
        return

    # Construir a matriz com bordas

    print(" _   " * 6)
    for i in range(6):
        # Linha superior das células

        
        # Linha com conteúdo das células
        linha = ""
        for j in range(6):
            if i == x and j == y:
                linha += "| X "  # Marca a posição especificada com 'X'
            elif i == xb and j == yb:
                linha += "| B "  # Marca a posição especificada com 'B'
            elif (i == xm and j == ym) and found_manteiga != [0,0]:
                linha += "| M "
            elif (i == xt and j == yt) and found_torradeira != [0,0]:
                linha += "| T "  
            else:
                linha += "|   "  # Célula vazia
        linha += "|"  # Final da linha
        print(linha)
        print(" _   " * 6)
    if x == xb and y == yb:
        deteta_bolor(True)
    # Linha inferior das células

#-------------------------------------------------------------------------------------------------------->
# Funções para calibrar sensor de cor
#-------------------------------------------------------------------------------------------------------->
def calibra_color_sensor(sensor):
    ev3.speaker.beep()  # Som para indicar o início da calibração
    print("Coloque o sensor sobre uma superfície branca e pressione o botão central.")
    
    # Espera até que o botão central seja pressionado para calibrar o preto
    while not any(ev3.buttons.pressed()):
        wait(10)
    branco = sensor.reflection()
    print("Reflexão no branco:", branco)
    wait(1000)  # Tempo para ajustar a posição
    ev3.speaker.beep()  # Som para indicar o início da calibração
    print("Coloque o sensor sobre uma superfície branca e pressione o botão central.")
    
    # Espera até que o botão central seja pressionado para calibrar o branco
    while not any(ev3.buttons.pressed()):
        wait(10)
    preto = sensor.reflection()
    print("Reflexão no preto:", preto)
    
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
# Função que deteta a cor e associa ao cheiro de um dos elementos
#-------------------------------------------------------------------------------------------------------->
#def cheirar():
    global next_dir_code
    global calor
    print("Cheirando")
    ev3.screen.clear() # Limpar a tela antes de desenhar
    ev3.screen.draw_text(5, 90, "Cheirando")
    while True:
        #verde -> bom caminho
        #castanho -> caminho mau 
        #if toqueSensor.pressed():
        if colorSensor.color() == Color.WHITE: #sentir calor 
            ev3.speaker.beep(400, 100) 
            calor = True
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
    global particulas_mas
    global localizacao_bolor
    caminhos = {
        "norte" : abs((localizacao[0] - (localizacao_bolor[0] - 1))) + abs((localizacao[1] - localizacao_bolor[1])), 
        "sul" : abs((localizacao[0] - (localizacao_bolor[0] + 1))) + abs((localizacao[1] - localizacao_bolor[1])),
        "este" : abs((localizacao[1] - (localizacao_bolor[1] + 1))) + abs((localizacao[0] - localizacao_bolor[0])),
        "oeste" : abs((localizacao[1] - (localizacao_bolor[1] - 1))) + abs((localizacao[0] - localizacao_bolor[0]))
    }
    min_local = 999 #menor distancia ao bolor
    if caminhos["norte"] < min_local:
        min_local = caminhos["norte"] #4
    if caminhos["sul"] < min_local:  #6
        min_local = caminhos["sul"] #4
    if caminhos["este"] < min_local: #6
        min_local = caminhos["este"] #4
    if caminhos["oeste"] < min_local: #4
        min_local = caminhos["oeste"] #4
    print("Distância até ao bolor: " + str(min_local))
    if min_local <= 1:
        particulas_mas = True
        print("A " + str(min_local) + " casas do bolor")
    if caminhos["norte"] == min_local:
        localizacao_bolor[0] -= 1
        print ("Bolor -> norte")
        print("Localização do bolor: " + str(localizacao_bolor))
        return 0
    elif caminhos["sul"] == min_local:
        localizacao_bolor[0] += 1
        print("Bolor -> sul")
        print("Localização do bolor: " + str(localizacao_bolor))
        return 0
    elif caminhos["este"] == min_local:
        localizacao_bolor[1] += 1
        print("Bolor -> este")
        print("Localização do bolor: " + str(localizacao_bolor))
        return 0
    elif caminhos["oeste"] == min_local:
        localizacao_bolor[1] -= 1
        print("Bolor -> oeste")
        print("Localização do bolor: " + str(localizacao_bolor))
        return 0
    
    #compara dist para ele ir pra a manteiga  
def preenchePosLegais():
    global posLegais
    if localizacao == [1,1]:
        posLegais = [2,3]
    elif localizacao == [1,6]:
        posLegais = [3,4]
    elif localizacao == [6,6]:  
        posLegais = [1,4]
    elif localizacao == [6,1]:
        posLegais = [1,2]
    elif localizacao[0] == 1:
        posLegais = [2,3,4]
    elif localizacao[0] == 6:
        posLegais = [1,2,4] 
    elif localizacao[1] == 1:
        posLegais = [1,2,3]
    elif localizacao[1]== 6:
        posLegais = [1,3,4]
    else:
        posLegais = [1,2,3,4]
       
        
                          
def passeando():
        tempDir = randint(0,len(posLegais)-1)
        posEscolhida = posLegais[tempDir]
        print("                        vo ir para aqui -> " + str(posEscolhida))
        print("conta: " + str(posEscolhida) + "-" + str(dir_code) + "=" + str(posEscolhida - dir_code))
        if (posEscolhida - dir_code) == 0:
            return 2
        elif (posEscolhida - dir_code) == 1:
            return 3
        elif (posEscolhida - dir_code) == -1:
            return 1
        else:
            return 4

def compara_dist():
    global next_dir_code
    global old_dist
    print("Distancia anterior da manteiga: " + str(old_dist))
    print("Caminho mais perto da manteiga")
    print("Distancia da manteiga: " + str(distancia_manteiga)) 
    preenchePosLegais()
    print("____________________________________________________________Posições Legais: " + str(posLegais))
    next_dir_code = passeando()
    if ja_tive_aqui_e_nao_gostei(next_dir_code):
       next_dir_code = passeando()
    print("Saida do compara_dist: " + str(next_dir_code))

def dist_manteiga():
    global next_dir_code
    global distancia_manteiga
    global old_dist #distancia anterior
    global calor
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
        if colorSensor.color() == Color.BLUE: #sentir calor 
            ev3.speaker.beep(400, 100) 
            calor = True
            print("Torradeira está perto") # 1 casa
            ev3.screen.clear() # Limpar a tela antes de desenhar
            ev3.screen.draw_text(5, 90, "Torradeira está perto")
            wait(2000)


def ja_tive_aqui_e_nao_gostei(nexta_direcao):
    localVirtual = localizacao
    if nexta_direcao == 1:
        localVirtual[0] -= 1
    elif nexta_direcao == 2:
        localVirtual[1] += 1
    elif nexta_direcao == 3:
        localVirtual[0] += 1
    elif nexta_direcao == 4:
        localVirtual[1] -= 1
    for k in range(len(os_cheiros_anteriores)):
        if os_cheiros_anteriores[k] == localVirtual:
            return True
    return False

def bigger_than_6(i, j):
    big = abs(localizacao[0] - i) + abs(localizacao[1] - j)
    if big > 6:
        big = 6
    return big

def bigger_than_6_2(element):
    big2 = abs(localizacao[0] - element[0]) + abs(localizacao[1] - element[1])
    if big2 > 6:
        big2 = 6
    return big2


def manteiga_triangulator():
    #print("Entrei no triangulador")
    global possible_manteiga
    global found_manteiga
    print("Distância anterior da manteiga: " + str(old_dist))
    if old_dist > distancia_manteiga: 
        #print("aproximando")
        if contador_rondas < 1:
            #print("first")
            for i in range(1,7):
                for j in range(1,7):
                    if bigger_than_6(i, j) == distancia_manteiga:
                        if not (i == 1 and j == 1):
                            possible_manteiga.append([i, j])
        else:
            #print("not first")
            for i, element in enumerate(possible_manteiga):
                if bigger_than_6_2(element) != distancia_manteiga:
                    possible_manteiga.pop(i)
                if element == localizacao_bolor:
                    possible_manteiga.pop(i)
        if len(possible_manteiga) == 1:
            print("found manteiga")
            found_manteiga = possible_manteiga[0]
            return True
        if len(possible_manteiga) == 0:
            print("I am confused about this :p")
            return True
    elif old_dist < distancia_manteiga:
        print("afastando")
        for i, element in enumerate(possible_manteiga):
                if bigger_than_6_2(element) != distancia_manteiga:
                    possible_manteiga.pop(i)
                if element == localizacao_bolor:
                    possible_manteiga.pop(i)    
        if len(possible_manteiga) == 1:
            found_manteiga = possible_manteiga[0]
            return True
    elif old_dist == distancia_manteiga:
        return False
    return False
        
def gonna_get_manteiga(alvo):
    #print("gonna get that manteiga")
    global next_dir_code
    if localizacao[0] != alvo[0]:
        if localizacao[0] > alvo[0]:
            if dir_code == 1:
                next_dir_code = 2
            elif dir_code == 2:
                next_dir_code = 1
            elif dir_code == 3:
                next_dir_code = 4
            elif dir_code == 4:
                next_dir_code = 3
        else:
            if dir_code == 1:
                next_dir_code = 4
            elif dir_code == 2:
                next_dir_code = 3
            elif dir_code == 3:
                next_dir_code = 2
            elif dir_code == 4:
                next_dir_code = 1
    elif localizacao[1] != alvo[1]:
        if localizacao[1] > alvo[1]:
            if dir_code == 1:
                next_dir_code = 1
            elif dir_code == 2:
                next_dir_code = 4
            elif dir_code == 3:
                next_dir_code = 3
            elif dir_code == 4:
                next_dir_code = 2
        else:
            if dir_code == 1:
                next_dir_code = 3
            elif dir_code == 2:
                next_dir_code = 2
            elif dir_code == 3:
                next_dir_code = 1
            elif dir_code == 4:
                next_dir_code = 4
    print("...............................vou ir pa: " + str(next_dir_code))
    if next_dir_code == 1:  # Turn left (counter-clockwise)
        change = -1
    elif next_dir_code == 2:  # No turn (keep the same direction)
        change = 0
    elif next_dir_code == 3:  # Turn right (clockwise)
        change = 1
    elif next_dir_code == 4:  # Turn 180° (reverse direction)
        change = 2
    next_absolute = (dir_code + change - 1) % 4 + 1
    if not (ver_o_futuro(next_absolute, "next") and ver_o_futuro(next_absolute, "this")):
        if not did_i_win(next_absolute):
            next_dir_code = random_menos_este_num(next_dir_code)

def did_i_win(next_absolute):
    localVirtual = [0, 0]
    localVirtual[0] = localizacao[0]
    localVirtual[1] = localizacao[1]
    if next_absolute == 1:
        localVirtual[0] -= 1
    if next_absolute == 2:
        localVirtual[1] += 1
    if next_absolute == 3:
        localVirtual[0] += 1
    if next_absolute == 4:
        localVirtual[1] -= 1
    if localVirtual == found_manteiga:
        return True
    return False



def gps(alvo):
    distancia = abs(localizacao[0] - alvo[0]) + abs(localizacao[1] - alvo[1])
    return distancia  

            
def random_menos_este_num (nao_te_quero):
    rand_num = randint(1,3)
    if nao_te_quero == 1:
        return rand_num+1
    elif nao_te_quero == 2:
        if rand_num != 1:
            return rand_num+1
        else:
            return rand_num
    elif nao_te_quero == 3:
        if rand_num != 2:
            return rand_num+1
        else:
            return rand_num
    elif nao_te_quero == 4:  
        return rand_num
        

def fugir_bolor():
    global next_dir_code

    bolor = gps(localizacao_bolor)
    manteiga = gps(found_manteiga)
    if (bolor < manteiga and found_manteiga != [0,0]) or found_manteiga != [0,0]:
        mindist = localizacao[0] - localizacao_bolor[0]
        
        if localizacao_bolor[0] - localizacao[0] < mindist:
            mindist = localizacao_bolor[0] - localizacao[0]

        if localizacao[1] - localizacao_bolor[1] < mindist:
            mindist = localizacao[1] - localizacao_bolor[1]

        if localizacao_bolor[1] - localizacao[1] < mindist:
            mindist = localizacao_bolor[1] - localizacao[1]
        #escolhe uma localização aleatoria para se afastar
        next_dir_code = random_menos_este_num(mindist)

        if not pode_andar():
             while True: #alexandra não vejas o while True (e foi o ADRENALINO :p que pos)
                next_dir_code = random_menos_este_num(mindist)
                if pode_andar():
                    break
        return 0

    elif bolor >= manteiga and found_manteiga != [0,0]: 
        gonna_get_manteiga(found_manteiga)
    else:
        gonna_get_manteiga(possible_manteiga[0])

def cruz(i):
    if ((posicoes_torradeira[i][0] == localizacao[0]+1 and posicoes_torradeira[i][1] == localizacao[1]) or 
                 (posicoes_torradeira[i][0] == localizacao[0]-1 and posicoes_torradeira[i][1] == localizacao[1]) or
                  (posicoes_torradeira[i][0] == localizacao[0] and posicoes_torradeira[i][1] == localizacao[1]+1) or
                   (posicoes_torradeira[i][0] == localizacao[0] and posicoes_torradeira[i][1] == localizacao[1]-1)):
        return True
    else:
        return False


def torradeira_onde_andas():
    global posicoes_torradeira
    global found_torradeira
    array_temp_torradeira = []
   
    if calor:
        print("tá quentinho")

    for i in range(len(posicoes_torradeira)):
        if (not(posicoes_torradeira[i][0] == localizacao_bolor[0] and posicoes_torradeira[i][1] == localizacao_bolor[1]) and 
        not (posicoes_torradeira[i][0] == localizacao[0] and posicoes_torradeira[i][1] == localizacao[1]) and 
        not (posicoes_torradeira[i][0] == found_manteiga[0] and posicoes_torradeira[i][1] == found_manteiga[1])): 
            if not calor:
                if  not (cruz(i)):
                    #print("Vendo posição: " + str(posicoes_torradeira[i]))
                    array_temp_torradeira.append(posicoes_torradeira[i]) 
            elif calor:
                
                if (cruz(i)):
                    #print("tá na cruz")
                    array_temp_torradeira.append(posicoes_torradeira[i])
        
    
    #print("Posições torradeira: " + str(posicoes_torradeira))            
    
    posicoes_torradeira = array_temp_torradeira

def a_que_cheirava_aqui():
    os_cheiros_anteriores.append([localizacao,distancia_manteiga])
    
def manteiga_favoravel():
    min_distancia = gps(possible_manteiga[0]) #distancia incializada com a 1 posição do array
    manteiga_favoravel_index = 0 # indice para guardar a posiç�o da manteiga mais perto
    for i in range(len(possible_manteiga)): # percorremos o array das possições possiveis da maneteiga
       if gps(possible_manteiga[i]) < min_distancia: # se a dist�ncia possivel atual for menor do que a possiç�o menor anterior
           min_distancia = gps(possible_manteiga[i]) #nova minima dist�nica
           manteiga_favoravel_index = i #guarda a menor dist�ncia
    return possible_manteiga[manteiga_favoravel_index] #retorna a posiç�o da manteiga mais perto

def ver_o_futuro(nexta_direcao, mode):
    #print("Tou vendo o futuro...")
    localVirtual = [0,0]
    localVirtual[0] = localizacao[0]
    localVirtual[1] = localizacao[1]
    if nexta_direcao == 1:
        localVirtual[0] -= 1
    elif nexta_direcao == 2:
        localVirtual[1] += 1
    elif nexta_direcao == 3:
        localVirtual[0] += 1
    elif nexta_direcao == 4:
        localVirtual[1] -= 1
    if mode == "next":
        caminhos = {
            "norte": abs((localVirtual[0] - (localizacao_bolor[0] - 1))) + abs((localVirtual[1] - localizacao_bolor[1])),
            "sul": abs((localVirtual[0] - (localizacao_bolor[0] + 1))) + abs((localVirtual[1] - localizacao_bolor[1])),
            "este": abs((localVirtual[1] - (localizacao_bolor[1] + 1))) + abs((localVirtual[0] - localizacao_bolor[0])),
            "oeste": abs((localVirtual[1] - (localizacao_bolor[1] - 1))) + abs((localVirtual[0] - localizacao_bolor[0]))
        }
    else:
        caminhos = {
            "norte": abs((localVirtual[0] - (localizacao_bolor[0]))) + abs((localVirtual[1] - localizacao_bolor[1])),
            "sul": abs((localVirtual[0] - (localizacao_bolor[0]))) + abs((localVirtual[1] - localizacao_bolor[1])),
            "este": abs((localVirtual[1] - (localizacao_bolor[1]))) + abs((localVirtual[0] - localizacao_bolor[0])),
            "oeste": abs((localVirtual[1] - (localizacao_bolor[1]))) + abs((localVirtual[0] - localizacao_bolor[0]))
        }
    min_local = 999  # menor distancia ao bolor
    if caminhos["norte"] < min_local:
        min_local = caminhos["norte"]  # 4
    if caminhos["sul"] < min_local:  # 6
        min_local = caminhos["sul"]  # 4
    if caminhos["este"] < min_local:  # 6
        min_local = caminhos["este"]  # 4
    if caminhos["oeste"] < min_local:  # 4
        min_local = caminhos["oeste"]  # 4
    if min_local == 0:
        return False
    return True


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
    if contador_rondas == 0: #calibrar sensor de cor
        print("Calibração concluída.")
    print("************* Ronda: " + str(contador_rondas) + " *************")
   


    if deteta_torradeira():
    

        if found_manteiga == [0,0]:
            dist_manteiga()
            manteiga_triangulator()
            #if possible_manteiga:
            gonna_get_manteiga(manteiga_favoravel())
            #else:
            #    compara_dist()
        else:
            print("indo para a manteiga")
            gonna_get_manteiga(found_manteiga)
            
        andar()
        print("Localizacao atual do robo: " + str(localizacao))  # imprimi a localização atual
        old_dist = distancia_manteiga


    if found_torradeira == [0,0]:
        torradeira_onde_andas()
    #else:
        #print("Posição Torradeira: " + str(found_torradeira))   
            
    bolor_calculator()
    print("Possiveis posições da manteiga" + str(possible_manteiga))
    contador_rondas += 1
    if localizacao_bolor == found_torradeira:
        if localizacao_bolor == localizacao:
            print("Bolor ganhou!")
        else:
            print("Bolor foi queimado!")
        break
    deteta_manteiga()
    if contador_rondas >= 25:
        print("Todos perderam por limite de rondas, sejam mais rapidos (robo e bolor)!")
        break
    mostrar_localizacao(localizacao, found_manteiga, found_torradeira)
    if found_manteiga != [0,0]:
        print("Distancia da manteiga vertical: " + str(abs(localizacao[0] - found_manteiga[0])) + " e dist�ncia da manteiga horizontal: " + str(abs(localizacao[1] - found_manteiga[1])))
    time.sleep(3)
    print("----------------------------------------------------------------->")
