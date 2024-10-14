#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Znap Program
------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-expansion
"""
from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick 
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint

ev3= EV3Brick()
middle_motor= Motor(Port.B)
right_motor = Motor(Port.C)
left_motor = Motor(Port.A)

middle_motor.run(1000)
wait(2000)
middle_motor.stop()

i = 0
while i < 2:
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(200, 100)  # C
    wait(100)
    ev3.speaker.beep(300, 250)  # D
    wait(200)
    ev3.speaker.beep(400, 100)  # E
    wait(250)
    i = i + 1

# Parte final da música
wait(100)
ev3.speaker.beep(400, 200)  # F
wait(200)
ev3.speaker.beep(400, 100)  # F
wait(100)
ev3.speaker.beep(350, 100)  # D
wait(100)
ev3.speaker.beep(350, 100)  # D
wait(100)
ev3.speaker.beep(300, 100)  # D
wait(100)
ev3.speaker.beep(300, 100)  # D
wait(100)
ev3.speaker.beep(200, 150)  # G
#FAZER MOVIMENTO
left_motor.run_angle(1000,-900)
speed = 500
left_motor.run(speed)
right_motor.run(speed)
wait(5000)
left_motor.stop()
right_motor.stop()
left_motor.run_angle(1000,900)

#MOVER A GARRA
middle_motor.run(-1000)
wait(2000)
middle_motor.stop()
