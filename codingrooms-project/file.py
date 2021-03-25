from pydraw import *
from classes import *
import random
import time


screen = Screen(800,600,"H")
screen.color(Color("black"))
# screen.grid(cellsize=(20,20))

########################
#                      #
#        Loading       #
#                      #
########################

load_outline = Rectangle(screen,screen.width()/2-100,screen.height()/2-20,200,40,fill=False,border=Color("White"))
load_outline.border(width=4)

load_bar = Rectangle(screen,screen.width()/2-100,screen.height()/2-20,1,40,color=Color("white"))


player_play = False
computer_play = False

first_click = True

#######################
#                     #
#       Tiles         #
#                     #
#######################

tile_size = 20
grid_width = 36
grid_height = 26

expected_num_of_tiles = grid_height*grid_width
loaded_tiles = 0
loaded_indices = 0

tile_list = []

for x in range(grid_width):
    for y in range(grid_height):
        tile = Tile(screen,2*tile_size+x*tile_size,2*tile_size+tile_size*y,tile_size)
        tile_list.append(tile)
        loaded_tiles+=1
        load_bar.width(200*(loaded_tiles/(2*expected_num_of_tiles)))
        screen.update()

for n in range(len(tile_list)):
    for i in range(len(tile_list)):
        if tile_list[n].rect.distance(tile_list[i].rect)<tile_size*1.5 and tile_list[n].rect.distance(tile_list[i].rect) != 0:
            tile_list[n].indices_in_range.append(i)
        if len(tile_list[n].indices_in_range) == 8:
            break
    loaded_indices+=1
    load_bar.width(200*((loaded_tiles+loaded_indices)/(2*expected_num_of_tiles)))
    screen.update()
    

print("Tiles loaded")

load_bar.visible(False)
load_outline.visible(False)

def toggle_board_visibility(show):
    for tile in tile_list:
        tile.rect.visible(show)




###########################
#                         #
#       MENU STUFF        #
#                         #
###########################


play_button = Menu_button(screen,0,0,"Play",txt_size=25)
play_button.center(screen.center())

computer_button = Menu_button(screen,0,0,"Computer",txt_size=25)
computer_button.center(screen.center())
computer_button.move(0,75)

title_text = Text(screen,"Minesweeper",0,0,color=Color("white"),size=35)
title_text.center(screen.center())
title_text.move(0,-75)

def menu_toggle(show):

    play_button.rect.visible(show)
    computer_button.rect.visible(show)
    title_text.visible(show)

    play_button.text.visible(show)
    computer_button.text.visible(show)



###############
#             #
#     gaem    #
#             #
###############



def make_bombs(bombs_wanted,location):
    bomb_count = 0
    while bomb_count < bombs_wanted:
        random_index = random.randrange(len(tile_list))
        while tile_list[random_index].bomb or tile_list[random_index].rect.distance(location)<tile_list[0].size*3:
            random_index = random.randrange(len(tile_list))
        tile_list[random_index].make_bomb()
        bomb_count+=1

    for tile in tile_list:
        for index in tile.indices_in_range:
            if tile_list[index].bomb:
                tile.bombs_in_range+=1


def zeroclear(tile):
    index_list = tile.indices_in_range.copy()
    print(len(tile.indices_in_range))
    while len(index_list)>0:
        init_len = len(index_list)

        for i in range(init_len):
            if not tile_list[index_list[i]].uncovered:
                if tile_list[index_list[i]].bombs_in_range == 0:
                    for new_index in tile_list[index_list[i]].indices_in_range:
                        index_list.append(new_index)
                tile_list[index_list[i]].click()
                screen.update()

        for i in range(init_len):
            index_list.pop(0)
    


def bomb_loss():
    for tile in tile_list:
        if tile.bomb:
            tile.rect.color(Color(0,0,0))
            screen.update()

    time.sleep(5)

    for tile in tile_list:
        tile.reset()
    toggle_board_visibility(False)
    menu_toggle(True)


def win_reset():
    for tile in tile_list:
        if tile.bomb:
            tile.rect.color(Color("green"))
            screen.update()
    
    time.sleep(1)

    for tile in tile_list:
        tile.reset()
    toggle_board_visibility(False)
    menu_toggle(True)


bombs_wanted = 100


def solver():
    global bombs_wanted,computer_play,player_play,first_click
    print("solving")
    make_bombs(bombs_wanted,tile_list[0].rect.center())
    screen.update()

    tile_list[0].click()
    screen.update()
    print(len(tile_list[0].indices_in_range))
    zeroclear(tile_list[0])
    screen.update()

    unsolved = True
    while unsolved:
        for tile in tile_list:
            if tile.uncovered and tile.bombs_in_range != 0:
                covered_count = 0
                
                for i in range(len(tile.indices_in_range)):
                    if not tile_list[tile.indices_in_range[i]].uncovered:
                        covered_count += 1
                
                if covered_count == tile.bombs_in_range:
                    for n in tile.indices_in_range:
                        if not tile_list[n].uncovered and not tile_list[n].flagged:
                            tile_list[n].flag()
                            screen.update()
                
        
        for tile in tile_list:
            if tile.uncovered and tile.bombs_in_range != 0:
                flagged_count = 0

                for i in range(len(tile.indices_in_range)):
                    if tile_list[tile.indices_in_range[i]].flagged:
                        flagged_count += 1
                
                if flagged_count == tile.bombs_in_range:
                    for n in tile.indices_in_range:
                        if not tile_list[n].uncovered and not tile_list[n].flagged:
                            tile_list[n].click()
                            if tile_list[n].bombs_in_range==0:
                                zeroclear(tile_list[n])
                            screen.update()

        uncovered_count = 0
        for tile in tile_list:
            if tile.uncovered:
                uncovered_count += 1
        
        if uncovered_count == len(tile_list) - bombs_wanted:
            unsolved = False
            time.sleep(2)
            win_reset()
            player_play = False
            computer_play = False
            first_click = True

def mousedown(button,location):
    global player_play, computer_play,first_click, bombs_wanted
    if title_text.visible():
        if play_button.contains(location):
            player_play = True
            menu_toggle(False)
            toggle_board_visibility(True)
            first_click = True
            
        elif computer_button.contains(location):
            computer_play = True
            menu_toggle(False)
            toggle_board_visibility(True)
            solver()



    elif not title_text.visible():

        for tile in tile_list:

            if not tile.uncovered and tile.contains(location):

                if first_click:
                    make_bombs(bombs_wanted,location)
                    first_click = False


                if button == 1 and not tile.flagged:
                    if not tile.bomb:
                        tile.click()
                        if tile.bombs_in_range == 0:
                            zeroclear(tile)
                    else:
                        bomb_loss()
                        player_play = False
                        computer_play = False
                        first_click = True
                    
                    total_uncovered = 0
                    for tile in tile_list:
                        if tile.uncovered:
                            total_uncovered +=1
                    if total_uncovered == len(tile_list) - bombs_wanted:
                        win_reset()
                        player_play = False
                        computer_play = False
                        first_click = True

                elif button == 3:
                    tile.flag()
                    

screen.listen()



screen.update()
screen.stop()