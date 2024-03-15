import math
import time
from math import cos, sin

import serial
import pygame

pygame.init()

WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])

arduinoData = serial.Serial('com19', 115200)
time.sleep(1)
timer = pygame.time.Clock()
fps = 60
data = [0, 0, 0, 0, 0]
font = pygame.font.Font('freesansbold.ttf', 24)


def parseData(input):
    # servo angle 0, state 1 2, state 2 2, state 3 2, state 4 2
    out = []  # angle, led bank1,2,3 and 4
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    index = 0
    if input[16] == ',':
        index = 1
    elif input[17] == ',':
        index = 2
    ang = input[14: 15 + index]
    for i in range(len(ang)):
        if ang[i] not in nums:
            ang = 0
    st1 = input[25 + index]
    if st1 not in nums:
        st1 = 0
    st2 = input[36 + index]
    if st2 not in nums:
        st2 = 0
    st3 = input[47 + index]
    if st3 not in nums:
        st3 = 0
    st4 = input[58 + index]
    if st4 not in nums:
        st4 = 0
    out = [ang, st1, st2, st3, st4]
    print(out)
    return out


def draw_screen(ins):
    print(ins)
    ins = [int(ins[0]), int(ins[1]), int(ins[2]), int(ins[3]), int(ins[4])]
    radius = 90
    xprime = 200 - radius * cos(ins[0] / 57.2958)
    yprime = 90 - radius * sin(ins[0] / 57.2958)
    print(xprime, yprime)
    screen.blit(font.render(f'angle: {ins[0]}*', True, 'dark gray'), (190, 10))
    pygame.draw.line(screen, 'white', (200, 90), (xprime, yprime), 10)
    pygame.draw.circle(screen, 'dark gray', (200, 90), 10)

    change = ['-5', '-10', '+5', '+10']

    for i in range(4):
        if ins[i + 1] == 3:
            pygame.draw.circle(screen, 'red', (50 + 100 * i, 160), 40)
            pygame.draw.circle(screen, 'green', (50 + 100 * i, 250), 40)
            pygame.draw.circle(screen, 'white', (50 + 100 * i, 340), 40)
        elif ins[i + 1] == 2:
            pygame.draw.circle(screen, 'red', (50 + 100 * i, 160), 40)
            pygame.draw.circle(screen, 'green', (50 + 100 * i, 250), 40)
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 340), 40)
        elif ins[i + 1] == 1:
            pygame.draw.circle(screen, 'red', (50 + 100 * i, 160), 40)
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 250), 40)
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 340), 40)
        else:
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 160), 40)
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 250), 40)
            pygame.draw.circle(screen, 'dark gray', (50 + 100 * i, 340), 40)
        screen.blit(font.render(f'{change[i]}', True, 'white'), (30 + 100 * i, 97))


run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    print(dataPacket)
    if len(str(dataPacket)) > 59:
        data = parseData(str(dataPacket))
    draw_screen(data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
pygame.quit()
