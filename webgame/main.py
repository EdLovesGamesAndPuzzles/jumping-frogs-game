import os
import asyncio
import pygame as pg
import sys
import copy
import math
#from pygame.local import  *


async def main():


    size = width, height = (1200,600)
    background_color = pg.Color("lightblue")# potential contenders are turqouise2, skyblue lightblue etc
    lilypad_num = 5
    position = 2
    radius = 10
    lijst = [1]*lilypad_num
    Rect = pg.Rect(0, 0, 100, 100)
    selected = False
    all_states = []
    all_states.append(lijst.copy())
    print(all_states)

    pg.init()
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Jumping Frogs")

    clock = pg.time.Clock()

    


    #apply changes
    pg.display.update()

    #load images
    frog = pg.image.load("frog-cartoon-sitting.png")
    print(frog.get_rect())
    frog = pg.transform.scale(frog, (40,40))
    frog_rect = pg.Rect(0,0,40,40)

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
                                all_states.append(lijst.copy())
                                print(all_states)

                    if event.key in [pg.K_d, pg.K_RIGHT] and selected == True:
                        if position + (lijst[position]*2 -1)< lilypad_num:
                            landing = position +(lijst[position]*2-1)
                            if lijst[landing] != 0:
                                lijst[landing] = lijst[landing] +lijst[position]
                                lijst[position] = 0
                                position = landing
                                selected = False
                                all_states.append(lijst.copy())
                                print(all_states)

                    if event.key in [pg.K_r]:
                        lijst = []
                        for i in range(0,lilypad_num):
                            lijst.append(1)
                        all_states = [lijst.copy()]

                    if event.key in [pg.K_z] and len(all_states) >1:
                        all_states.pop()
                        lijst = all_states[-1].copy()
                        #all_states = copy.deepcopy(all_states)
                        position = math.ceil(lilypad_num/2) -1
                        print(all_states)

                        
                            

                        


        screen.fill(background_color)

        #Draw lilypads
        
        lilypad_w = int(min(width/lilypad_num - 10, 200))
        for i in range(0,lilypad_num):
            pg.draw.rect(screen, (0, 100, 0), ((i+0.5)*width/lilypad_num - 0.5*lilypad_w, int(0.8*height), lilypad_w, 10)) 

        #Draw arrow above
        Rect.center = ((position+0.5)*width/lilypad_num, 0.3*height+selected*0.1*height)
        screen.blit(arrow,Rect)

        #Draw the frogs
        for i in range(0, lilypad_num):
            for ii in range(0,lijst[i]):
                frog_rect.center = (i + 0.5)*width/lilypad_num, 0.8*height-20 -(40*ii)
                screen.blit(frog, frog_rect)
                #pg.draw.circle(screen, (100,255,0), ((i+0.5)*width/lilypad_num, 0.8*height-radius-(2*radius *ii)), radius)

        if max(lijst) == lilypad_num:
            print("You win")
            print("Next level")
            lilypad_num += 1
            lijst = []
            for i in range(0,lilypad_num):
                lijst.append(1)
            all_states = [lijst.copy()]
            print(all_states)
    

        await asyncio.sleep(0)
        
        pg.display.update()
                    



    pg.quit()

asyncio.run(main())

#########################



