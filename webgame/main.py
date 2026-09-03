import os
import asyncio
import pygame as pg
import math
#from pg.local import  *


# async is needed for webapp
async def main():


    size = width, height = (1280,720)
    background_color = pg.Color("lightblue")# This sets the background color. Potential contenders are turqouise2, skyblue lightblue etc
    lilypad_num = 5 # Amount of lilypad at the starting level
    lilypad_w = int(min(width/lilypad_num - 10, 250))
    lilypad_h = 30
    frog_w = lilypad_w//2.5
    position = 2 # position of the selector
    lijst = [1]*lilypad_num #Starting position of the frogs
    Rect = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
    selected = False #Has the player selected anything. Start of as False
    all_states = [lijst.copy()] #The current level is one
    How_to_play_screen = False


    #initialize Pygame
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()


    #apply changes
    pg.display.update()

    #load images
    pond = pg.image.load("pond.png").convert_alpha()
    pond = pg.transform.scale(pond, (width, height)).convert_alpha()
    pond_rect = pg.Rect(0,0,width,height)


    frog = pg.image.load("frog.png").convert_alpha()
    frog = pg.transform.scale(frog, (frog_w,frog_w)).convert_alpha()
    frog_rect = pg.Rect(0,0,frog_w,frog_w)

    Lilypad = pg.image.load("lilypad.png").convert_alpha()
    lilypad = pg.transform.scale(Lilypad, (lilypad_w, 30)).convert_alpha()
    lilypad_rect = pg.Rect(0,0,lilypad_w, 30)

    arrow = pg.image.load("arrow.png").convert_alpha()
    arrow = pg.transform.scale(arrow, (100, 100)).convert_alpha()
    arrow_loc = arrow.get_rect()
    arrow_loc.center = 0.5*width/lilypad_num, height*0.2


    #Main loop
    running = True
    while running:
        clock.tick(60)
        
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if How_to_play_screen == False:
                    if event.type == pg.KEYDOWN:
                        if event.key in [pg.K_a, pg.K_LEFT] and selected == False:
                            if position != 0:
                                position = position -1
                                Rect.move_ip(-(width/lilypad_num), 0)
                        elif event.key in [pg.K_d, pg.K_RIGHT] and selected == False:
                            if position != lilypad_num -1:
                                position = position +1
                                #Rect.move_ip(width/lilypad_num, 0)
                        elif event.key in [pg.K_s, pg.K_DOWN] and lijst[position]!=0:
                            selected = True
                        elif event.key in [pg.K_w, pg.K_UP]:
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
                                    

                        if event.key in [pg.K_d, pg.K_RIGHT] and selected == True:
                            if position + (lijst[position]*2 -1)< lilypad_num:
                                landing = position +(lijst[position]*2-1)
                                if lijst[landing] != 0:
                                    lijst[landing] = lijst[landing] +lijst[position]
                                    lijst[position] = 0
                                    position = landing
                                    selected = False
                                    all_states.append(lijst.copy())
                                    

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

                else:
                    if event.type == pg.KEYDOWN:
                        if event.key in [pg.K_c]:
                            How_to_play_screen = False
                        

         
                            

                        

        #Drawing part of the loop

        #screen.fill(background_color)
        screen.blit(pond, pond_rect)

        #Draw lilypads
        if How_to_play_screen == False:
            for i in range(0,lilypad_num):
                #pg.draw.rect(screen, (0, 100, 0), ((i+0.5)*width/lilypad_num - 0.5*lilypad_w, int(0.8*height), lilypad_w, 10)) 
                lilypad_rect.center = ((i+0.5)*width/lilypad_num, int(0.8*height))
        
                screen.blit(lilypad, lilypad_rect)


            #Draw arrow above
            Rect.center = ((position+0.5)*width/lilypad_num, 0.3*height+selected*0.1*height)
            screen.blit(arrow,Rect)

            #Draw the frogs
            for i in range(0, lilypad_num):
                for ii in range(lijst[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*width/lilypad_num, 0.8*height-(frog_w*ii))
                    screen.blit(frog, frog_rect)

            if max(lijst) == lilypad_num:
                print("You win")
                print("Next level")
                lilypad_num += 1
                lijst = [1]*lilypad_num
                all_states = [lijst.copy()]
                lilypad_w = int(min(width/lilypad_num - 10, 200))
                lilypad_rect = pg.Rect(0,0,lilypad_w, 30)
                lilypad = pg.transform.scale(Lilypad, (lilypad_w, 30)).convert_alpha()
                frog_w = lilypad_w//2.5
            
    

        await asyncio.sleep(0)
        
        pg.display.update()
                    



    pg.quit()

asyncio.run(main())

#########################