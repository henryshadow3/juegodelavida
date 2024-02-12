import pygame as pg
import numpy as np
import time

pg.init()

width, height = 650, 650
screen = pg.display.set_mode((width, height))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 50, 50

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

# Inicialización de algunas celdas en estado "vivo"


pauseExec = False

while True:
    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    ev = pg.event.get()

    for event in ev:
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        elif event.type == pg.KEYDOWN:
            pauseExec = not pauseExec

    mouseClick = pg.mouse.get_pressed()
    if sum(mouseClick) > 0:
        posX, posY = pg.mouse.get_pos()
        celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
        if mouseClick[0]:  # Click izquierdo
            gameState[celX, celY] = 1
        elif mouseClick[2]:  # Click derecho
            gameState[celX, celY] = 0

    for y in range(0, nyC):
        for x in range(0, nxC):
            if not pauseExec:
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + gameState[(x) % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x) % nxC, (y + 1) % nyC] + gameState[(x + 1) % nxC, (y + 1) % nyC]

                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [(x * dimCW, y * dimCH),
                    ((x + 1) * dimCW, y * dimCH),
                    ((x + 1) * dimCW, (y + 1) * dimCH),
                    (x * dimCW, (y + 1) * dimCH)]

            color = (128, 128, 128) if gameState[x, y] == 0 else (255, 255, 255)
            pg.draw.polygon(screen, color, poly, 0 if gameState[x, y] == 1 else 1)

    if not pauseExec:
        gameState = np.copy(newGameState)

    pg.display.flip()
