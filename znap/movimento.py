import urandom

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.media.ev3dev import Image, ImageFile, SoundFile
from pybricks.tools import wait, StopWatch

ev3= EV3Brick()
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.D)

localizacao = [1,1]
direcao = "frente"

speed = 500

def andar():
    left_motor.run(speed)
    right_motor.run(speed)
    wait(1850)
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
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    left_motor.run_angle(1000, -680)
    if direcao == "frente":
        direcao = "direita"
    if direcao == "direita":
        direcao = "atras"
    if direcao == "atras":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "frente"

def rodar_esquerda():
    left_motor.run(speed)
    right_motor.run(speed)
    wait(700)
    left_motor.stop()
    right_motor.stop()
    right_motor.run_angle(1000, -680)
    if direcao == "frente":
        direcao = "esquerda"
    if direcao == "esquerda":
        direcao = "atras"
    if direcao == "atras":
        direcao = "direita"
    if direcao == "direita":
        direcao = "frente"


