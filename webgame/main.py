import os
import asyncio
import pygame as pg
import math
import button
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
    arrow_rect = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
    selected = False #Has the player selected anything. Start of as False
    all_states = [lijst.copy()] #The current level is one
    game_state = "home" #game states are "home", "htp", "playing", "won"


    #initialize Pygame
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()
    my_font = pg.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('Congrats! You won this level! Press any key to continue', False, (0, 0, 0))


    #apply changes
    pg.display.update()

    #load images
    pond_original = pg.image.load("pond.png").convert_alpha()
    pond = pg.transform.scale(pond_original, (width, height)).convert_alpha()
    pond_rect = pg.Rect(0,0,width,height)

    htp_original = pg.image.load("HTP-screen.png").convert_alpha()
    htp = pg.transform.scale(htp_original, (width, height)).convert_alpha()
    htp_rect = pg.Rect(0,0,width,height)

    frog_original = pg.image.load("frog.png").convert_alpha()
    frog = pg.transform.scale(frog_original, (frog_w,frog_w)).convert_alpha()
    frog_rect = pg.Rect(0,0,frog_w,frog_w)

    Lilypad_original = pg.image.load("lilypad.png").convert_alpha()
    lilypad = pg.transform.scale(Lilypad_original, (lilypad_w, 30)).convert_alpha()
    lilypad_rect = pg.Rect(0,0,lilypad_w, 30)

    arrow_original = pg.image.load("arrow.png").convert_alpha()
    arrow = pg.transform.scale(arrow_original, (100, 100)).convert_alpha()
    arrow_loc = arrow.get_rect()
    arrow_loc.center = 0.5*width/lilypad_num, height*0.2


    #Now for the buttons
    play_img_original = pg.image.load("play_button.png").convert_alpha()
    htp_img_original = pg.image.load("How_to_play_button.png").convert_alpha()

    play_button = button.Button(100,200, play_img_original, 0.1)
    htp_button = button.Button(100,400, htp_img_original, 0.1)


    #Main loop
    running = True
    while running:
        clock.tick(60)
        
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:

                    if game_state == "htp":
                        game_state = "home"

                    if game_state == "won":
                        game_state = "playing"

                    if game_state == "playing":
                        if event.key in [pg.K_a, pg.K_LEFT] and selected == False:
                            if position != 0:
                                position = position -1
                                arrow_rect.move_ip(-(width/lilypad_num), 0)
                        elif event.key in [pg.K_d, pg.K_RIGHT] and selected == False:
                            if position != lilypad_num -1:
                                position = position +1
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

                        if event.key in [pg.K_m]:
                            game_state = "home"
                        

         
                            

                        

        #Drawing part of the loop

        #screen.fill(background_color)
        

        if game_state == "home":
            screen.blit(pond,pond_rect)
            if play_button.draw(screen) ==True:
                game_state = "playing"
            if htp_button.draw(screen) == True:
                game_state = "htp"


        if game_state == 'htp':
            screen.blit(htp, htp_rect)

        
        if game_state == "playing":

            #Fill background
            screen.blit(pond, pond_rect)
            #Draw lilypads
            for i in range(0,lilypad_num): 
                lilypad_rect.center = ((i+0.5)*width/lilypad_num, int(0.8*height))
                screen.blit(lilypad, lilypad_rect)

            #Draw arrow above
            arrow_rect.center = ((position+0.5)*width/lilypad_num, 0.3*height+selected*0.1*height)
            screen.blit(arrow, arrow_rect)

            #Draw the frogs
            for i in range(0, lilypad_num):
                for ii in range(lijst[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*width/lilypad_num, 0.8*height-(frog_w*ii))
                    screen.blit(frog, frog_rect)

            if max(lijst) == lilypad_num and game_state == "playing":
                lilypad_num += 1
                lijst = [1]*lilypad_num
                all_states = [lijst.copy()]
                lilypad_w = int(min(width/lilypad_num - 10, 200))
                lilypad_rect = pg.Rect(0,0,lilypad_w, 30)
                lilypad = pg.transform.scale(Lilypad_original, (lilypad_w, 30)).convert_alpha()
                frog_w = lilypad_w//2.5
                game_state = "won"
                screen.blit(text_surface, (0,0))



            
    

        await asyncio.sleep(0)
        
        pg.display.update()
                    



    pg.quit()

asyncio.run(main())

#########################