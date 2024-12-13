#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from random import randint, random
import sys
import time

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
    if localizacao_manteiga == localizacao_bolor:
        print("Derrotado pelo bolor")
        sys.exit()  
    elif  localizacao_manteiga == localizacao:
        print("O robô esta: " + str(localizacao))
        print("Manteiga encontrada")
        sys.exit()  
    

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_bolor(aux):
    if  localizacao == localizacao_bolor or aux == True or localizacao_manteiga == localizacao_bolor:
        print("Derrotado pelo bolor")
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    global contador_rondas
    global localizacao_torradeira
    global ja_esperou
    if  (localizacao == localizacao_torradeira and ja_esperou):
        #localizacao_torradeira = [0,0]
        #contador_rondas+=1
        ja_esperou = False
        print("A torradeira está a tostar homem tosta")
        return False
    ja_esperou = True
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
    #print(str(dir_code) + "atual")
    #print(str(next_dir_code) + "next")
    global posLegais
    if localizacao[0] <= 1: #se encontra-se no 1 quadrado/primeira linha e testa para a norte
        if dir_code == 2 and next_dir_code == 1:
            return False
        if dir_code == 4 and next_dir_code == 3:
            return False
        if dir_code == 1 and next_dir_code == 2:
            return False
        #print("passei do localização[0]")    
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
        #print("passei do localizacao[1]")   
    return True
#---------------------------------------------------fim pode_andar------------------------------------>


#------------------------------------------------------------------------------------------------------> 
#       Função deteta_barreira deteta as barreiras e tenta evita-las
#------------------------------------------------------------------------------------------------------> 
def deteta_barreira():
    global next_dir_code
    for i in barreiras:
        if dir_code == 1:
            if  localizacao[0] == barreiras[i][0]+0.5 and localizacao[1] == barreiras[i][1]:
                print("Barreira encontrada")
                mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
                if not pode_andar():
                    if next_dir_code == 1:
                        next_dir_code = 3
                    elif next_dir_code == 3:
                        next_dir_code = 1
                verifica_se_quer_virar() #chama para virar
        if dir_code == 2:
            if  localizacao[0] == barreiras[i][0] and localizacao[1] == barreiras[i][1]-0.5:
                print("Barreira encontrada")
                mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
                if not pode_andar():
                    if next_dir_code == 1:
                        next_dir_code = 3
                    elif next_dir_code == 3:
                        next_dir_code = 1
                verifica_se_quer_virar() #chama para virar
        if dir_code == 3:
            if  localizacao[0] == barreiras[i][0]-0.5 and localizacao[1] == barreiras[i][1]:
                print("Barreira encontrada")
                mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
                if not pode_andar():
                    if next_dir_code == 1:
                        next_dir_code = 3
                    elif next_dir_code == 3:
                        next_dir_code = 1
                verifica_se_quer_virar() #chama para virar
        if dir_code == 4:
            if  localizacao[0] == barreiras[i][0] and localizacao[1] == barreiras[i][1]+0.5:
                print("Barreira encontrada")
                mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
                if not pode_andar():
                    if next_dir_code == 1:
                        next_dir_code = 3
                    elif next_dir_code == 3:
                        next_dir_code = 1
                verifica_se_quer_virar() #chama para virar




#---------------------------------------------------fim Deteta_barreira-------------------------------->



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
# Função rodar_direita que faz o robo girar à sul e atualiza a direção
#------------------------------------------------------------------------------------------------------>
def rodar_direita():
    global direcao
    global dir_code
    dir_code = (dir_code % 4) + 1
    if direcao == "este":  # se o robo estava virado para a este fica virado para a sul
        direcao = "sul"
    elif direcao == "sul": # se o robo estava virado para a sul fica virado para a trás
        direcao = "oeste"
    elif direcao == "norte":
        direcao = "este"
    elif direcao == "oeste": # se o robo estava virado para trás fica virado para a norte
        direcao = "norte"

 # se o robo estava virado para a este fica virado para a norte

 #---------------------------------------------------fim rodar_direita----------------------------------->
 
 
#--------------------------------------------------------------------------------------------------------> 
# Função rodar_esquerda 
#-------------------------------------------------------------------------------------------------------->
def rodar_esquerda():
    global direcao
    global dir_code

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

def deteta_barreira_1():
    barreiras_fixas_ao_descer = [[2, 3], [3, 4], [4, 3], [5, 6]]
    barreiras_fixas_a_direita = [2, 5]
    global next_dir_code
    for i in range(4):
        #print(localizacao)
        #print(barreiras_fixas_ao_descer[i])
        if localizacao == barreiras_fixas_ao_descer[i] or localizacao == barreiras_fixas_a_direita:
            #vira para a sul       
            mini_rand_dir()   # escolhe uma direção aleatória esq ou dir
            if not pode_andar():
                if next_dir_code == 1:
                    next_dir_code = 3
                elif next_dir_code == 3:
                    next_dir_code = 1
            verifica_se_quer_virar() #chama para virar 
            break
            

#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç o selecionada, ir  andar nessa direç o e atualizar a sua posiç o
#-------------------------------------------------------------------------------------------------------->
def andar():
    print("Direção robô:  " + direcao + " code -> " + str(dir_code))
    verifica_se_quer_virar()

    deteta_barreira_1()
    
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
def mostrar_localizacao(localizacao, localizacao_manteiga, localizacao_torradeira):
    # Obter as coordenadas x e y da posição, ajustando para índice zero
    x, y = localizacao[0] - 1, localizacao[1] - 1
    xb, yb = localizacao_bolor[0] - 1, localizacao_bolor[1] - 1
    xm, ym = localizacao_manteiga[0] - 1, localizacao_manteiga[1] - 1
    xt, yt = localizacao_torradeira[0] - 1, localizacao_torradeira[1] - 1
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
            elif i == xm and j == ym:
                linha += "| M "
            elif i == xt and j == yt:
                linha += "| T "  
            else:
                linha += "|   "  # Célula vazia
        linha += "|"  # Final da linha
        print(linha)
    if x == xb and y == yb:
        deteta_bolor(True)
    # Linha inferior das células
    print(" _   " * 6)

         
# Código para a matriz do bolor
def bolor_calculator():
    global particulas_mas
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
    print("Distancia anteriror da manteiga: " + str(old_dist))
    '''
    if old_dist < distancia_manteiga:
        print("Caminho mais longe da manteiga")
        print("Distancia atual da manteiga: " + str(distancia_manteiga))
        print("Casas de distância da manteiga: " + str(distancia_manteiga))
        retry = True
        while retry:       
            mini_rand_dir()
            
            if pode_andar():
                retry = False
    elif old_dist >= distancia_manteiga:
    '''
    print("Caminho mais perto da manteiga")
    print("Distancia da manteiga: " + str(distancia_manteiga)) 
    preenchePosLegais()
    print("____________________________________________________________Posições Legais: " + str(posLegais))
    next_dir_code = passeando()
    if ja_tive_aqui_e_nao_gostei(next_dir_code):
        next_dir_code = passeando()

    '''
        rand_dir() #da uma direção 
        if ((localizacao[1] == 6 and dir_code == 2) or (localizacao[0] == 6 and dir_code == 3) or 
            (localizacao[1] == 1 and dir_code == 4) or (localizacao[0] == 1 and dir_code == 1)):
            if not pode_andar() or ja_tive_aqui_e_nao_gostei(next_dir_code):
                print("Não posso andar")
                rand_dir()   # escolhe uma direção aleatória esq ou dir
                countingWhiles = 0
                while not pode_andar() and ja_tive_aqui_e_nao_gostei(next_dir_code): # Leandro não esteve aqui
                    countingWhiles +=1 
                    if countingWhiles < 3:
                        rand_dir()
                    else:
                        while not pode_andar():
                            rand_dir()
                            '''
    print("Saida do compara_dist: " + str(next_dir_code))

def dist_manteiga():
    global next_dir_code

    global distancia_manteiga
    global old_dist #distancia anterior
    global calor
    #print("Cheirando")
    #while True:
    try:
        # Solicitar entrada do cheiro da manteiga
        #entrada = int(input("Cheirando 1-6 (0 sair): "))
        entrada = gps(localizacao_manteiga)

        # Verificar a entrada e atualizar a variável
        if entrada == 0:
            print("Saindo...")
            #break
        elif entrada == 1:
            distancia_manteiga = 1
            
        elif entrada == 2:
            distancia_manteiga = 2
            
        elif entrada == 3:
            distancia_manteiga = 3
            
        elif entrada == 4:
            distancia_manteiga = 4
            
        elif entrada == 5:
            distancia_manteiga = 5
            
        elif entrada == 6:
            distancia_manteiga = 6
            
        else:
            print("Entrada inválida. Digite um número entre 1 e 6.")
    
    except ValueError:

            print("Por favor, insira um número válido.")
    
    try:
        '''
        # Solicitar entrada do usuário
        entrada = int(input("Cheiro torradeira 1 (1 casa)(0 sair): "))
        # Verificar a entrada e atualizar a variável
        if entrada == 0:
            #print("Saindo...")
            break
        elif entrada == 1:
            print("Torradeira está perto") # 1 casa
            calor = True
            break
        '''

    except ValueError:

        print("Por favor, insira um número válido.")
            
    #compara_dist() #não elim   



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
    for i in range(len(os_cheiros_anteriores)):
        if os_cheiros_anteriores[i] == localVirtual:
            return True
    return False
#---->
def barreiras():
    global barreiras
    for i in range(5):
        barreiras = []
        if randint(1,2) == 1:
            barreiras.append([random.randint(1, 5)+0.5, random.randint(1, 6)])
        else:
            barreiras.append([random.randint(1, 6), random.randint(1, 5)+0.5])

def manteiga_triangulator():
    #print("Entrei no triangulador")
    global possible_manteiga
    global found_manteiga
    print("Distância anterior da manteiga: " + str(old_dist))
    if old_dist > distancia_manteiga: 
        print("aproximando")
        if contador_rondas <= 1:
            print("first")
            for i in range(1,6):
                for j in range(1,6):
                    if modulo(localizacao[0] - i) + modulo(localizacao[1] - j) == distancia_manteiga:
                        if not (localizacao[0] == 1 and localizacao[1] == 1):
                            possible_manteiga.append([i, j])
        else:
            print("not first")
            for i, element in enumerate(possible_manteiga):
                if (modulo(localizacao[0] - element[0]) + modulo(localizacao[1] - element[1])) != distancia_manteiga:
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
                if (modulo(localizacao[0] - element[0]) + modulo(localizacao[1] - element[1])) != distancia_manteiga:
                    possible_manteiga.pop(i)
                if element == localizacao_bolor:
                    possible_manteiga.pop(i)    
        if len(possible_manteiga) == 1:
            found_manteiga = possible_manteiga[0]
            return True
    elif old_dist == distancia_manteiga:
        #print("Muito longe mesmo")
        return False
    return False
        
def gonna_get_manteiga(alvo):
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

def gps(alvo):
    distancia = modulo(localizacao[0] - alvo[0]) + modulo(localizacao[1] - alvo[1])
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
    #possivel razao do problema
    if (bolor < manteiga and found_manteiga != [0,0]) or found_manteiga != [0,0]:

    #if (bolor < manteiga and found_manteiga != [0,0]) or found_manteiga == [0,0]:
        # procura qual direção é a que está mais proxima
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
    #temp_n_calor = []
    #temp_n_calor.append(localizacao[0], localizacao[1] - 1) 
    #temp_n_calor.append(localizacao[0] + 1, localizacao[1]) 
    #temp_n_calor.append(localizacao[0], localizacao[1] + 1) 
    #temp_n_calor.append(localizacao[0] - 1, localizacao[1]) 
    
    #print("posiçoes possiveis pre copiar: " + str(posicoes_torradeira)) 

    if not deteta_torradeira():# o robo está na torradeira
        found_torradeira = localizacao
        return 0
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
        
    
    print("Posições torradeira: " + str(posicoes_torradeira))            
                
    #print("Array temporario: " + str(array_temp_torradeira))
    
    posicoes_torradeira = array_temp_torradeira
    
    #print("estou a pensar nas posicoes da torradeira")     

    #print("Possível posições torradeira: " + str(posicoes_torradeira)) 




def a_que_cheirava_aqui():
    os_cheiros_anteriores.append(localizacao,distancia_manteiga)
    

            
#-------------------------------------------------------------------------------------------------------->
# Ciclo de teste de código
#-------------------------------------------------------------------------------------------------------->

localizacao_manteiga = [randint(2, 5),randint(2, 5)]
localizacao_torradeira = [randint(2, 5),randint(2, 5)]#.ap2
print("info dev localização torradeira:" + str(localizacao_torradeira))

while True:
    if contador_rondas == 0: #calibrar sensor de cor
         print("Calibração concluída.")
    if gps(localizacao_torradeira) == 1:
        calor = True
    else:
        calor = False
    print("************* Ronda: " + str(contador_rondas) + " *************")
   
    if found_torradeira == [0,0]:
        torradeira_onde_andas()
    else:
        print("Posição Torradeira: " + str(found_torradeira))
        
    if deteta_torradeira():
        retry = True
        if contador_rondas == 0:
            while retry:        
                rand_dir()          # decidir uma direção aleatória
                if pode_andar():
                    retry = False
        else:
            if particulas_mas and not ((modulo(localizacao[0] - found_manteiga[0]) + modulo(localizacao[1] - found_manteiga[1])) < 2):
                #print("Fugindo")
                print("cheiro: " + str(gps(localizacao_manteiga)))
                dist_manteiga()
                fugir_bolor()
                time.sleep(5)
            elif found_manteiga == [0,0]:
                #print("Manteigando")
                print("cheiro: " + str(gps(localizacao_manteiga)))
                dist_manteiga()
                if (possible_manteiga != []):
                    gonna_get_manteiga(possible_manteiga[0])
                else:
                    compara_dist()
            else:
                gonna_get_manteiga(found_manteiga)
               
        #print("nao saio daqui")
        #print(pode_andar())
        manteiga_triangulator()
        while pode_andar():
            andar()
            break             # movimenta-se para a direção
        if deteta_manteiga():
            break
        if deteta_bolor(False):
            break
        print("Localizacao atual do robo: " + str(localizacao))  # imprimi a localização atual
    bolor_calculator()
    print("Possiveis posições da manteiga" + str(possible_manteiga))
    
    contador_rondas += 1
    old_dist = distancia_manteiga
    if localizacao_bolor == localizacao_torradeira:
        if localizacao_bolor == localizacao:
            print("Bolor ganhou!")
        else:
            print("Bolor foi queimado!")
        break
    if localizacao_manteiga == localizacao_bolor:
        #print("A manteiga foi comida")
        deteta_manteiga()
        break
    if contador_rondas >= 25:
        print("Todos perderam por limite de rondas, sejam mais rapidos (robo e bolor)!")
        break
    mostrar_localizacao(localizacao, localizacao_manteiga, localizacao_torradeira)
    #if found_manteiga != [0,0]:
    time.sleep(5)
    print("----------------------------------------------------------------->")
