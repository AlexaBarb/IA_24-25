from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.hubs import EV3Brick
from pybricks.tools import wait


# Lista que armazenará os símbolos associados às cores detetadas (por exemplo, "+", "*", etc.).
pecas = []
ev3 = EV3Brick() 

# Sensor de cor
sensorCor = ColorSensor(Port.S1) 

# Deteta a cor passada no sensor de cores
def detetaCor():
    # Lê o valor da cor
    corDetetada = sensorCor.color()

    # Mapa de valores de cor para nomes de cor
    listaCores = {
        Color.BLUE: 'Azul',
        Color.GREEN: 'Verde',
        Color.YELLOW: 'Amarelo',
        Color.RED: 'Vermelho',
    }

    # Determina a cor detectada
    nomeCorDetetada = listaCores.get(corDetetada, 'Desconhecida')
    # Retorna o nome da cor detectada
    return nomeCorDetetada

# Deteta a cor das peças passadas e adiciona no array das peças
def detetaCorPecas():
    # Lê o nome da cor
    corDetetada = detetaCor()
    # Imprime a cor lida
    print('Cor detectada: ' + corDetetada)

    # Adiciona a peça no array dependendo da cor
    if corDetetada == 'Verde':
        pecas.append("+")
        ev3.speaker.say("Green")
        
    elif corDetetada == 'Vermelho':
        pecas.append("*")
        ev3.speaker.say("Red")
        
    elif corDetetada == 'Amarelo':
        pecas.append("0")
        ev3.speaker.say("Yellow")
        
    elif corDetetada == 'Azul':
        pecas.append("-")
        ev3.speaker.say("Blue")

# Período da deteção de peças            
def leituraObjetos():
    # Enquanto está no período de deteção
    while True:
        # Deteta e guarda as peças
        detetaCorPecas()
        # Espera 2 segundos
        wait(2000)

# Iniciar a leitura de objetos
leituraObjetos()
print(detetaCorPecas())
