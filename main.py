import os
import pygame as pg
#from pygame.local import  *

size = width, height = (800,600)
vijver_h = int(height/1.6)

pg.init()
running = True
screen = pg.display.set_mode(size)

pg.display.set_caption("Edwins first game")
screen.fill((60,220, 0))
#draw graphics
pg.draw.rect(screen, (50,50,50), (0, height/2 - vijver_h/2, width, vijver_h))


#apply changes
pg.display.update()


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False



pg.quit()


