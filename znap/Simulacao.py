#!/usr/bin/env pybricks-micropython

#------------------------------------------------------------------------------------------------------> 
#                           imports das bibliotecas necessárias
#------------------------------------------------------------------------------------------------------> 
from random import randint, random
import sys


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
localizacao_torradeira = [3,3] #localização da torradeira
localizacao_manteiga = [5,2] #localização da manteiga
distancia_manteiga = 11 #distancia da manteiga 0 - 10
old_dist = 11 #antiga distancia da manteiga
manteiga = [0,0]
torradeira = [0,0]
barreiras = []
#---------------------------------------------------fim Inicio------------------------------------------> 


#------------------------------------------------------------------------------------------------------> 
#       Função deteta_manteaiga_bolor deteta  manteiga e agarra-a, ou se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_manteiga():
    if  manteiga == localizacao:
        print("Manteiga encontrada")
        sys.exit()
    

#---------------------------------------------------fim Deteta_agarra_manteiga-------------------------> 

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_bolor deteta se encontrar o bolor fica triste e desiste
#------------------------------------------------------------------------------------------------------> 
def deteta_bolor(aux):
    if  localizacao == localizacao_bolor or aux == True:
        print("Derrotado pelo bolor")
        sys.exit()
#---------------------------------------------------fim deteta_bolor----------------------------------->

#------------------------------------------------------------------------------------------------------> 
#       Função deteta_torradeira se encontrar a torradeira espera 5 segundos a torrar
#------------------------------------------------------------------------------------------------------> 
def deteta_torradeira():
    global contador_rondas
    global torradeira
    if  localizacao == torradeira:
        torradeira = [0,0]
        contador_rondas+=1
        print("A torradeira está a tostar homem tosta")
        return False
    return True    
        
#----------------------------------------------fim deteta_torradeira----------------------------------->

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


#------------------------------------------------------------------------------------------------------> 
# Função pode_andar retorna um booleano usa uma string direção para testar se pode andar
#------------------------------------------------------------------------------------------------------> 
def pode_andar(): #função que verifica se é possível andar na direção indicada
    #print(str(dir_code) + "atual")
    #print(str(next_dir_code) + "next")
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
        #print("passei do localização[1]")   
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
    if next_dir_code != 2: #tem de virar mas não precisa de fazer 180
        if next_dir_code == 1:
            rodar_esquerda()
            print("Vira para a esquerda: code -> " + str(dir_code) + " direção -> " + direcao)
        else:
            rodar_direita()
            print("Vira para a direita: code -> " + str(dir_code) + " direção -> " + direcao)

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
            break;
            

#-------------------------------------------------------------------------------------------------------->
# Função anda que, caso poder andar na direç o selecionada, ir  andar nessa direç o e atualizar a sua posiç o
#-------------------------------------------------------------------------------------------------------->
def andar():
    print("Direção atual:  " + direcao + " code -> " + str(dir_code))
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
    while True:
        try:
            # Solicitar entrada do usuário
            entrada = int(input("Cheirando 1-6 (0 sair): "))
            
            # Verificar a entrada e atualizar a variável
            if entrada == 0:
                print("Saindo...")
                break
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
            # Solicitar entrada do usuário
            entrada = int(input("Cheiro torradeira 1 (1 casa)(0 sair): "))
            # Verificar a entrada e atualizar a variável
            if entrada == 0:
                print("Saindo...")
                break
            elif entrada == 1:
                print("Torradeira está perto") # 1 casa

        except ValueError:

            print("Por favor, insira um número válido.")    
                
    compara_dist()

def compara_dist():
    global next_dir_code
    global old_dist
    print("Distancia anteriror da manteiga: " + str(old_dist))
    if old_dist < distancia_manteiga:
        old_dist = distancia_manteiga
        print("Caminho mais longe da manteiga")
        print("Distancia atual da manteiga: " + str(distancia_manteiga))
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
               
def barreiras():
    global barreiras
    for i in range(5):
        barreiras = []
        if randint(1,2) == 1:
            barreiras.append([random.randint(1, 5)+0.5, random.randint(1, 6)])
        else:
            barreiras.apped([random.randint(1, 6), random.randint(1, 5)+0.5])

    

#-------------------------------------------------------------------------------------------------------->
# Ciclo de teste de código
#-------------------------------------------------------------------------------------------------------->
manteiga = input("Inserir a localização da manteira [x,y]: ")
torradeira = input("Inserir localização da torradeira [x,y]: ")
#barreiras() erro
while True:
    if contador_rondas == 0: #calibrar sensor de cor
         print("Calibração concluída.")

    print("************* Ronda: " + str(contador_rondas) + " *************")
    
    if deteta_torradeira():
        retry = True
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
    contador_rondas += 1

    print("----------------------------------------------------------------->")
