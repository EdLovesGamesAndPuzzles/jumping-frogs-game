import os
import asyncio
import pygame as pg
import math
import button


def player_has_won(current_state):
    return max(current_state) == sum(current_state)

def get_landing_index(arrow_index, frog_count, direction):
    distance = 2 * frog_count -1

    if direction == "left":
        return arrow_index -distance
    elif direction == "right":
        return arrow_index + distance

def is_valid_landing(landing_index, current_state):
    if landing_index >=0 and landing_index <len(current_state):
        if current_state[landing_index] > 0:
            return True
    return False

def draw_lilypads(screen, width, height, image, lilypad_count):
    for i in range(0,lilypad_count):
        lilypad_rect = image.get_rect()
        lilypad_rect.center = ((i+0.5)*width//lilypad_count, int(0.8*height))
        screen.blit(image, lilypad_rect)

def draw_arrow(screen, width, height, image, arrow_index, lilypad_count, is_selected):
    arrow_rect = image.get_rect()
    arrow_rect.center = ((arrow_index+0.5)*width/lilypad_count, 0.3*height+is_selected*0.1*height)
    screen.blit(image, arrow_rect)


    
    

# async is needed for webapp
async def main():

    size = width, height = (1280,720)
    background_color = pg.Color("lightblue")# This sets the background color. Potential contenders are turqouise2, skyblue lightblue etc
    lilypad_count = 5 # Amount of lilypad at the starting level
    lilypad_width = int(min(width/lilypad_count - 10, 250))
    lilypad_height = 70
    frog_width = 102
    arrow_index = 2 # position of the selector
    current_state = [1]*lilypad_count #Starting position of the frogs
    arrow_rect = pg.Rect(0, 0, 100, 100) #dummy variable, later used for selector
    is_selected = False #Has the player selected anything. Start of as False
    state_history = [current_state.copy()] #This memories all the previous states of the game at that level to enable undoing with z
    game_state = "home" #game states are "home", "htp", "playing", "won"
    indicator_scalar = 1.4 #F stands for factor, which is the factor by which the indicator width and height are multiplied by the width and height of the lilypad
    clicked = False

    #initialize Pygame
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Jumping Frogs")
    clock = pg.time.Clock()
    my_font = pg.font.SysFont("Comic Sans MS", 30)
    
    #apply changes
    pg.display.update()


    def start_level(level_number):

        nonlocal lilypad_count
        nonlocal lilypad_width
        nonlocal lilypad_rect
        nonlocal lilypad
        nonlocal indicator
        nonlocal indicator_rect
        nonlocal current_state
        nonlocal state_history
        nonlocal arrow_index
        nonlocal is_selected
        nonlocal game_state


        lilypad_count = level_number + 4

        current_state = [1] * lilypad_count
        state_history = [current_state.copy()]

        arrow_index = lilypad_count // 2
        is_selected = False
        game_state = "playing"


        lilypad_width = int(min(width/lilypad_count - 10, 200))
        lilypad_rect = pg.Rect(0,0,lilypad_width, lilypad_height)
        lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
        indicator = pg.transform.scale(indicator_original, (int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar)))
        indicator_rect = pg.Rect(0,0,int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar))

   



    level_rects = []

    start_x = 330
    start_y = 222

    spacing_x = 127
    spacing_y = 94

    button_width = 116
    button_height = 82

    for row in range(4):
        for col in range(5):

            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            rect = pg.Rect(
                x,
                y,
                button_width,
                button_height
            )

            level_rects.append(rect)

    level_to_home_button_rect = pg.Rect(1045, 605, 206, 74)

    #load images
    screen_rect = pg.Rect(0,0,width, height)

    pond_original = pg.image.load("pond.png").convert_alpha()
    pond = pg.transform.scale(pond_original, (width, height))
    pond_rect = pond.get_rect()

    htp_original = pg.image.load("HTP-screen.png").convert_alpha()
    htp = pg.transform.scale(htp_original, (width, height))
    htp_rect = htp.get_rect()

    homescreen_original = pg.image.load("Homescreen.png").convert_alpha()
    homescreen = pg.transform.scale(homescreen_original, (width, height))
    homescreen_rect = homescreen.get_rect()

    levelscreen_original = pg.image.load("level_screen.png").convert_alpha()
    levelscreen = pg.transform.scale(levelscreen_original, (width, height))
    levelscreen_rect = levelscreen.get_rect()

    title_original = pg.image.load("name_of_game.png").convert_alpha()
    title = pg.transform.scale(title_original, (250,200))
    title_rect = title.get_rect()

    frog_original = pg.image.load("frog.png").convert_alpha()
    frog = pg.transform.scale(frog_original, (frog_width,frog_width))
    frog_rect = frog.get_rect()

    Lilypad_original = pg.image.load("lilypad.png").convert_alpha()
    lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
    lilypad_rect = lilypad.get_rect()


    indicator_original = pg.image.load("landing_indicator2.png").convert_alpha()
    visible_rect = indicator_original.get_bounding_rect()
    indicator_original = indicator_original.subsurface(visible_rect).copy()
    indicator = pg.transform.scale(indicator_original, (int(lilypad_width *indicator_scalar), int(lilypad_height*indicator_scalar)))
    indicator_rect = indicator.get_rect()


    arrow_original = pg.image.load("arrow.png").convert_alpha()
    arrow = pg.transform.scale(arrow_original, (100, 100))
    arrow_loc = arrow.get_rect()
    arrow_loc.center = 0.5*width/lilypad_count, height*0.2

    wooden_sign_original = pg.image.load("wooden_sign.png").convert_alpha()
    wooden_sign = pg.transform.scale(wooden_sign_original, (1000, 600))
    wooden_sign_rect = wooden_sign.get_rect()
    wooden_sign_rect.midtop = (640, -100)

    menu_button_original = pg.image.load("menu_button.png").convert_alpha()
    menu_button = pg.transform.scale(menu_button_original, (250,126))
    menu_button_rect = menu_button.get_rect()
    menu_button_rect.topright = (1270,0)

    #Now for the buttons
    # play_img_original = pg.image.load("play_button.png").convert_alpha()
    # htp_img_original = pg.image.load("How_to_play_button.png").convert_alpha()
    # levels_img_original = pg.image.load("levels_button.png").convert_alpha()
    # credits_img_original = pg.image.load("credits_button.png").convert_alpha()

    # play_button = button.Button(100,200, play_img_original, 0.1)
    # htp_button = button.Button(100,400, htp_img_original, 0.1)
    # levels_button = button.Button(600, 200, levels_img_original, 0.1)
    # credits_button = button.Button(600, 400, credits_img_original, 0.1)


    play_button_rect = pg.Rect(472, 332, 343, 90)
    htp_button_rect = pg.Rect(472, 447, 343, 77)
    levels_button_rect = pg.Rect(472,554, 343, 77)




    #Main loop
    running = True
    while running:
        clock.tick(60)


        pos = pg.mouse.get_pos()
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if game_state == "levels":
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:

                            for index, rect in enumerate(level_rects):

                                if rect.collidepoint(event.pos):

                                    level_number = index + 1

                                    print("Selected level:", level_number)
                                    start_level(level_number)
                                    
                            if level_to_home_button_rect.collidepoint(pos):
                                game_state = "home"


                if event.type == pg.KEYDOWN:

                    if game_state == "htp":
                        game_state = "home"

                    elif game_state == "won":
                        game_state = "playing"

                    elif game_state == "playing":
                        if event.key in [pg.K_a, pg.K_LEFT] and is_selected == False:
                            if arrow_index != 0:
                                arrow_index = arrow_index -1
                                arrow_rect.move_ip(-(width/lilypad_count), 0)
                        elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == False:
                            if arrow_index != lilypad_count -1:
                                arrow_index = arrow_index +1
                        elif event.key in [pg.K_s, pg.K_DOWN] and current_state[arrow_index]!=0:
                            is_selected = True
                        elif event.key in [pg.K_w, pg.K_UP]:
                            is_selected = False

                        elif event.key in [pg.K_a, pg.K_LEFT] and is_selected == True:

                            landing_index = get_landing_index(arrow_index, current_state[arrow_index],"left")
                            if is_valid_landing(landing_index, current_state) == True:
                                current_state[landing_index] = current_state[landing_index] +current_state[arrow_index]
                                current_state[arrow_index] = 0
                                arrow_index = landing_index
                                is_selected = False
                                state_history.append(current_state.copy())

                        elif event.key in [pg.K_d, pg.K_RIGHT] and is_selected == True:

                            landing_index = get_landing_index(arrow_index, current_state[arrow_index],"right")
                            if is_valid_landing(landing_index, current_state) == True:
                                current_state[landing_index] = current_state[landing_index] +current_state[arrow_index]
                                current_state[arrow_index] = 0
                                arrow_index = landing_index
                                is_selected = False
                                state_history.append(current_state.copy())
                                    
                        #r is restart
                        elif event.key in [pg.K_r]:
                            current_state = [1]*lilypad_count
                            state_history = [current_state.copy()]
                            is_selected = False
                            arrow_index = math.ceil(lilypad_count/2) -1

                        #z is undo
                        elif event.key in [pg.K_z] and len(state_history) >1:
                            state_history.pop()
                            current_state = state_history[-1].copy()
                            is_selected = False
                            arrow_index = math.ceil(lilypad_count/2) -1

                        #m returns to menu
                        elif event.key in [pg.K_m]:
                            game_state = "home"
                            is_selected = False
                            arrow_index = math.ceil(lilypad_count/2) -1
                        


         
          

                        

        #Drawing part of the loop

        #screen.fill(background_color)
        

        if game_state == "home":
            
            #check mouseover and clicked conditions
            if play_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "playing"
            elif htp_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "htp"
            elif levels_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "levels"

            if pg.mouse.get_pressed()[0] == 0:
                clicked = False

            screen.blit(homescreen, homescreen_rect)

        elif game_state == "htp":
            screen.blit(htp, screen_rect)

        elif game_state == "levels":
            screen.blit(levelscreen, levelscreen_rect)

            # for i in range(0,len(level_rects)):
            #     pg.draw.rect(screen, "red", level_rects[i], 3)

            # pg.draw.rect(screen, "red", level_to_home_button_rect, 3)
    

            mouse_pos = pg.mouse.get_pos()

            for rect in level_rects:

                if rect.collidepoint(pos):

                    pg.draw.ellipse(
                        screen,
                        (255, 255, 100),
                        rect,
                        4
                    )




        
        if game_state == "playing" or game_state == "won":

            #Fill background
            screen.blit(pond, pond_rect)

            #Menu button
            screen.blit(menu_button, menu_button_rect)

            if menu_button_rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and clicked == False:
                    clicked = True
                    game_state = "home"
            if pg.mouse.get_pressed()[0] == 0:
                clicked = False

            #Draw lilypads
            if is_selected == True:
                indicator_left = get_landing_index(arrow_index, current_state[arrow_index], "left")
                indicator_right = get_landing_index(arrow_index, current_state[arrow_index], "right")
                if is_valid_landing(indicator_left, current_state):
                    indicator_rect.center = ((indicator_left + 0.5) * width//lilypad_count, int(0.8*height))
                    screen.blit(indicator, indicator_rect)
                if is_valid_landing(indicator_right, current_state):
                    indicator_rect.center = ((indicator_right + 0.5)*width//lilypad_count, int(0.8*height))
                    screen.blit(indicator,indicator_rect)

            draw_lilypads(screen, width, height, lilypad, lilypad_count)

            #Draw arrow above
            draw_arrow(screen, width, height, arrow, arrow_index, lilypad_count, is_selected)

            #Draw the frogs
            if lilypad_count <= 10:
                frog_stack_spacing = int(0.5*frog_width)
            else:
                 frog_stack_spacing = int(0.42*frog_width)
            for i in range(0, lilypad_count):
                for ii in range(current_state[i]-1, -1, -1):
                    frog_rect.midbottom = ((i + 0.5)*width/lilypad_count, 0.8*height-(frog_stack_spacing*ii))
                    screen.blit(frog, frog_rect)

            if player_has_won(current_state) and game_state == "playing":
                lilypad_count += 1
                current_state = [1]*lilypad_count
                state_history = [current_state.copy()]
                lilypad_width = int(min(width/lilypad_count - 10, 200))
                lilypad_rect = pg.Rect(0,0,lilypad_width, lilypad_height)
                lilypad = pg.transform.scale(Lilypad_original, (lilypad_width, lilypad_height))
                indicator = pg.transform.scale(indicator_original, (int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar)))
                indicator_rect = pg.Rect(0,0,int(lilypad_width*indicator_scalar), int(lilypad_height*indicator_scalar))
                game_state = "won"
                
        if game_state == "won":
            screen.blit(wooden_sign, wooden_sign_rect)

            # sign_rect = pg.Rect(400, 200, 480, 200)
            # pg.draw.rect(screen, "brown", sign_rect)
            text_surface1 = my_font.render("Congrats! You win level "+ str(lilypad_count-5) + "!", False, (0, 0, 0))
            text_surface2 = my_font.render("Press any key to continue to level  "+ str(lilypad_count-4) + ".", False, (0, 0, 0))
            
            screen.blit(text_surface1, (434, 123))
            screen.blit(text_surface2, (434, 232))

            



        if pg.mouse.get_pressed()[0] == 1 and clicked == False:
            clicked = True
            print(pos)

        if pg.mouse.get_pressed()[0] == 0:
            clicked = False      

            
    

        await asyncio.sleep(0)

        pg.display.update()
    pg.quit()
asyncio.run(main())