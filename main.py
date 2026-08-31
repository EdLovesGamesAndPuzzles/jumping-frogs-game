import os
import pygame as pg
import sys
#from pygame.local import  *

size = width, height = (1200,600)

pg.init()
screen = pg.display.set_mode(size)

pg.display.set_caption("Jumping Frogs")

clock = pg.time.Clock()

lilypad_num = 6
position = 2
radius = 10
lijst = []
for i in range(0,lilypad_num):
     lijst.append(1)
Rect = pg.Rect(0, 0, 100, 100)

selected = False


#apply changes
pg.display.update()

#load images
frog = pg.image.load("frog-cartoon-sitting.png")

arrow = pg.image.load("arrow.png")
arrow = pg.transform.scale(arrow, (100, 100))
arrow_loc = arrow.get_rect()
arrow_loc.center = 0.5*width/lilypad_num, height*0.2

running = True
while running:
    clock.tick(60)
    
    for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_a, pg.K_LEFT] and selected == False:
                    if position != 0:
                        position = position -1
                        Rect.move_ip(-(width/lilypad_num), 0)
                elif event.key in [pg.K_r, pg.K_RIGHT] and selected == False:
                     if position != lilypad_num -1:
                          position = position +1
                          #Rect.move_ip(width/lilypad_num, 0)
                elif event.key in [pg.K_DOWN] and lijst[position]!=0:
                     selected = True
                elif event.key in [pg.K_UP]:
                     selected = False

                if event.key in [pg.K_a, pg.K_LEFT] and selected == True:
                    if position - (lijst[position]*2 -1)>= 0:
                        landing = position -(lijst[position]*2-1)
                        if lijst[landing] != 0:
                            lijst[landing] = lijst[landing] +lijst[position]
                            lijst[position] = 0
                            position = landing
                            selected = False

                if event.key in [pg.K_d, pg.K_RIGHT] and selected == True:
                    if position + (lijst[position]*2 -1)< lilypad_num:
                        landing = position +(lijst[position]*2-1)
                        if lijst[landing] != 0:
                            lijst[landing] = lijst[landing] +lijst[position]
                            lijst[position] = 0
                            position = landing
                            selected = False

                if event.key in [pg.K_r]:
                     lijst = []
                     for i in range(0,lilypad_num):
                          lijst.append(1)

                      
                          

                     


    screen.fill((0,0, 200))

    #Draw lilypads
    
    lilypad_w = int(min(width/lilypad_num - 10, 200))
    for i in range(0,lilypad_num):
        pg.draw.rect(screen, (0, 100, 0), ((i+0.5)*width/lilypad_num - 0.5*lilypad_w, int(0.8*height), lilypad_w, 10)) 

    #Draw arrow above
    Rect.center = ((position+0.5)*width/lilypad_num, 0.1*height+selected*0.1*height)
    screen.blit(arrow,Rect)

    #Draw the frogs
    for i in range(0, lilypad_num):
        for ii in range(0,lijst[i]):
            pg.draw.circle(screen, (100,255,0), ((i+0.5)*width/lilypad_num, 0.8*height-radius-(2*radius *ii)), radius)

    if max(lijst) == lilypad_num:
         print("You win")
         print("Next level")
         lilypad_num += 1
         lijst = []
         for i in range(0,lilypad_num):
              lijst.append(1)
   


    
    pg.display.update()
                



pg.quit()

#########################



