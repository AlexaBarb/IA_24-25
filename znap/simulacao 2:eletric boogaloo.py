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
def gps(alvo):
    distancia = modulo(localizacao[0] - alvo[0]) + modulo(localizacao[1] - alvo[1])
    return distancia

def modulo(a):
    if a < 0:
        return -a
    else:
        return a


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

    print(" _   " * 6)
    for i in range(6):
        # Linha superior das células

        # Linha com conteúdo das células
        linha = ""
        for j in range(6):
            for k in range(len(barreiras_fixas_a_direita)):
                if i == barreiras_fixas_a_direita[k][0] and j == barreiras_fixas_a_direita[k][1]:
                    linha += "/"
                    continue
            if i == x and j == y:
                linha += "| X "  # Marca a posição especificada com 'X'
            elif i == xb and j == yb:
                linha += "| B "  # Marca a posição especificada com 'B'
            elif i == xm and j == ym:
                linha += "| M "
            elif i == xt and j == yt:
                linha += "| T "
            else:
                linha += "|   "  # Célula vazia
        linha += "|"  # Final da linha
        print(linha)
        no_barrier_here = False
        for k in range(len(barreiras_fixas_ao_descer)):
            if i == (barreiras_fixas_ao_descer[k][0] - 1):
                linha_aqui = ""
                linha_aqui += "____" * (barreiras_fixas_ao_descer[k][1] - 1)
                linha_aqui += "****"
                linha_aqui += "____" * (6 - barreiras_fixas_ao_descer[k][1])
                print(linha_aqui)
                no_barrier_here = True
        if not no_barrier_here:
            print(" _   " * 6)



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
        print('torradeira_onde_andas()')
    else:
        print("Posição Torradeira: " + str(found_torradeira))

    mostrar_localizacao(localizacao, localizacao_manteiga, localizacao_torradeira)
    time.sleep(5)
    print("----------------------------------------------------------------->")