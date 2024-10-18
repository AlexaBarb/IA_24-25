rom pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, InfraredSensor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint

#inicializar o Eve3 
ev3= EV3Brick()
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.A)

Cor_Sensor = ColorSensor(Port.S1)

#cor barreiras -> vermelho
#cor linhas -> preto
#cor limitação de ambiente -> verde
while True:
    print(Cor_Sensor.color())
    #Se o sensor de cor detectar a cor preta, o robô andará para frente
    if Cor_Sensor.color() == Cor_Sensor.COLOR_BLACK:
        speed = 500
        left_motor.run(speed)
        right_motor.run(speed)
        wait(5000)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar outra cor, da uma volta 
    elif Cor_Sensor.color() == None :
        left_motor.run_angle(1000,-900)
        left_motor.stop()
        right_motor.stop()
    #Se o sensor de cor detectar a cor vermelha/barreira, o robô dará uma volta
    elif Cor_Sensor.color() == Cor_Sensor.COLOR_RED :
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()
    elif Cor_Sensor.color() == Cor_Sensor.COLOR_BROWN:
        left_motor.run_angle(1000,900)
        left_motor.stop()
        right_motor.stop()
