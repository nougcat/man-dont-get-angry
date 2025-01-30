import pygame
from first_run import first_run
from time import sleep
import json
import logging
import requests
import random
from copy import deepcopy
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HIGHT = 800


BASE_URL="http://localhost:2137"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set_caption('Chińczyk (Chinese)')

run = True
first_run_bool = True
waiting_for_players_to_join = True
whos_turn_is_it = -1
player_order = -1
player_colors = [(255,0,0),(0,0,255),(0,255,0),(255,255,0)]

# where x is tuple, and y is float
shade_of_color = lambda x, y: (x[0]*y, x[1]*y, x[2]*y)

# drawing pawns on the field
def drawing_pawns(screen, color, x,y, square_size, how_many):
    i = how_many
    while i > 0:
        if i == 1:
            pygame.draw.circle(screen, (255,255,255), (x+square_size/4, y+square_size/4), square_size//4)
            pygame.draw.circle(screen, color, (x+square_size/4, y+square_size/4), square_size//5)
        if i == 2:
            pygame.draw.circle(screen, (255,255,255), (x+square_size/4*3, y+square_size/4), square_size//4)
            pygame.draw.circle(screen, color, (x+square_size/4*3, y+square_size/4), square_size//5)
        if i == 3:
            pygame.draw.circle(screen, (255,255,255), (x+square_size/4, y+square_size/4*3), square_size//4)
            pygame.draw.circle(screen, color, (x+square_size/4, y+square_size/4*3), square_size//5)
        if i == 4:
            pygame.draw.circle(screen, (255,255,255), (x+square_size/4*3, y+square_size/4*3), square_size//4)
            pygame.draw.circle(screen, color, (x+ square_size/4*3 , y+square_size/4*3), square_size//5)
        if i >4:
            raise ValueError("Too many pawns on one field")
        i-=1

def get_pawns_location(board):
    temp_board = deepcopy(board)
    pawns = []
    for x in range(len(temp_board)-1):
        while temp_board[x] > 0:
            pawns.insert(0,x)
            temp_board[x] -= 1
        x = len(temp_board)-1
        while temp_board[x] > 0: # pawns that aren't on board
            pawns.append((x))
            temp_board[x] -= 1
    return pawns


font = pygame.font.Font(None, 36)
while run:
    # making blank screen
    screen.fill((0, 0, 0))
    if first_run_bool:
        (player_id, player_order, number_of_players) = first_run()
        first_run_bool = False
        dice_roll = -1
        chinczyk_board = [
            [0, 0, 0, 0, 9, 10, 11, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 51, 12, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 52, 13, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 53, 14, 0, 0, 0, 0],
            [1, 2, 3, 4, 5, 54, 15, 16, 17, 18, 19],
            [40, 41, 42, 43, 44,  0, 64, 63, 62, 61, 20],
            [39, 38, 37, 36, 35, 74, 25, 24, 23, 22, 21],
            [0, 0, 0, 0, 34, 73, 26, 0, 0, 0, 0],
            [0, 0, 0, 0, 33, 72, 27, 0, 0, 0, 0],
            [0, 0, 0, 0, 32, 71, 28, 0, 0, 0, 0],
            [0, 0, 0, 0, 31, 30, 29, 0, 0, 0, 0]
        ]
        # to get real index you have to substruct it b 1 (except for 0, which are empty/null)

    # check if game is won
    if not waiting_for_players_to_join and not first_run_bool:
        resp = requests.get(BASE_URL + "/game_won")
        if resp.status_code == 200:
            winner = resp.json()['message']
            print(f'winner={winner}')
            while winner == player_order:
                winner = resp.json()['message']
                screen.fill((0, 0, 0))
                text = font.render("You've won! Congratulations!", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HIGHT//2))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break

            while winner != -1:
                screen.fill((0, 0, 0))
                text = font.render("You've lost! Better luck next time!", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HIGHT//2))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        break


    # Drawing a chessboard
    square_size = 40
    for row in range(11):
        for col in range(11):
            x = col * square_size + (SCREEN_WIDTH - 400) // 2
            y = row * square_size + (SCREEN_HIGHT - 400) // 2
            if chinczyk_board[row][col]:
                match chinczyk_board[row][col]:
                    # 1, 11, 21, 31 are starting fields
                    # 41, 51, 61, 71 are last fields 
                    # other are just normal fields
                    case 1:
                        pygame.draw.rect(screen, shade_of_color(player_colors[0],2/3), (x, y, square_size, square_size))
                    case 41|42|43|44:
                        pygame.draw.rect(screen, shade_of_color(player_colors[0],1/2), (x, y, square_size, square_size))
                    case 11:
                        pygame.draw.rect(screen, shade_of_color(player_colors[1],2/3), (x, y, square_size, square_size))
                    case 51|52|53|54:
                        pygame.draw.rect(screen, shade_of_color(player_colors[1],1/2), (x, y, square_size, square_size))
                    case 21 if number_of_players > 2:
                        pygame.draw.rect(screen, shade_of_color(player_colors[2],2/3), (x, y, square_size, square_size))
                    case 61|62|63|64:
                        pygame.draw.rect(screen, shade_of_color(player_colors[2],1/2), (x, y, square_size, square_size))
                    case 31 if number_of_players > 3:
                        pygame.draw.rect(screen, shade_of_color(player_colors[3],2/3), (x, y, square_size, square_size))
                    case 71|72|73|74:
                        pygame.draw.rect(screen, shade_of_color(player_colors[3],1/2), (x, y, square_size, square_size))
                    case _:
                        pygame.draw.rect(screen, (255, 255, 255), (x, y, square_size, square_size))
            
    # drawing corners (players)
    pygame.draw.rect(screen, player_colors[0], (0, 0, square_size, square_size))
    pygame.draw.rect(screen, player_colors[1], (0, SCREEN_HIGHT-square_size, square_size, square_size))
    if number_of_players > 2:
        pygame.draw.rect(screen, player_colors[2], (SCREEN_HIGHT-square_size, 0, square_size, square_size))
        if number_of_players > 3:
            pygame.draw.rect(screen, player_colors[3], (SCREEN_HIGHT-square_size, SCREEN_HIGHT-square_size, square_size, square_size))
    
    # displaying pawns
    if not waiting_for_players_to_join:
        resp = requests.get(BASE_URL + "/game_board")
        if resp.status_code == 200:
            remote_chinczyk_board = json.loads(resp.json())
            # drawing pawns in homebase
            for i in range(4):
                match i:
                    # each player base has to be rendered
                    case 0:
                        drawing_pawns(screen, player_colors[i], 0, 0, square_size, remote_chinczyk_board[str(i)][74])
                    case 1:
                        drawing_pawns(screen, player_colors[i], 0, SCREEN_WIDTH-square_size, square_size, remote_chinczyk_board[str(i)][74])
                    case 2 if number_of_players > 2:
                        drawing_pawns(screen, player_colors[i], SCREEN_HIGHT-square_size, 0, square_size, remote_chinczyk_board[str(i)][74])
                    case 3 if number_of_players > 3:
                        drawing_pawns(screen, player_colors[i], SCREEN_HIGHT-square_size, SCREEN_WIDTH-square_size, square_size, remote_chinczyk_board[str(i)][74])


            # drawing a pawns on a board
            for player in range(number_of_players):
                for k in range(74):
                    if remote_chinczyk_board[str(player)][k]:
                        for row in range(11):
                            for col in range(11):
                                x = col * square_size + (SCREEN_WIDTH - 400) // 2
                                y = row * square_size + (SCREEN_HIGHT - 400) // 2
                                # if k is in not safe zone - so when k is between (0,70)
                                if k < 39+player*10:
                                    if chinczyk_board[row][col] == k%40+1:
                                        drawing_pawns(screen, player_colors[player], x, y, square_size,
                                        remote_chinczyk_board[str(player)][k])
                                else:
                                    if chinczyk_board[row][col] == k-(3-player)*10+1:
                                        drawing_pawns(screen, player_colors[player], x, y, square_size,
                                        remote_chinczyk_board[str(player)][k])


            
        # draw_pawns(screen, player_color_1, 0, 0, square_size, 4) # displaying pawns on just one field
        # draw_pawns(screen, player_color_2, 0, SCREEN_WIDTH-square_size, square_size, 1)
    # displaying pawns on just one field

    # waiting for other player turn, or just checking all of that, once in a while
    if player_order != whos_turn_is_it and not waiting_for_players_to_join:
        text = font.render("Waiting for other player turn...", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        resp = requests.get(BASE_URL + "/game_turn")
        try:
            whos_turn_is_it = resp.json()['message']
            if whos_turn_is_it != player_order:
                sleep(0.3)
            else:
                continue
        except Exception as e:
            logging.error("When requesting for game_turn, something went wrong")

    # rolling a dice
    if not dice_roll in {1,2,3,4,5,6}:
        dice_roll = random.randint(1, 6)        
    
    # doing a turn
    if player_order == whos_turn_is_it and not waiting_for_players_to_join:
        dice_text = font.render(f"You've rolled: {dice_roll}", True, (255, 255, 255))
        screen.blit(dice_text, (SCREEN_WIDTH//2 - dice_text.get_width()//2, 50))
        pygame.display.update()
        if dice_roll != 6 and remote_chinczyk_board[str(player_order)][74] + remote_chinczyk_board[str(player_order)][73] == 4:
            text = font.render(f"You've rolled {dice_roll}, your turn has been be skipped", True, (255, 0, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HIGHT//2))
            pygame.display.update()
            dice_roll = -1
            # to make this project better to present i made this 4 second sleep
            sleep(1)
            # if you want to make this game more smooth delete it

            resp = requests.get(BASE_URL + "/skip_turn?client_id=" + str(player_id))
            try:
                if resp.status_code == 200:
                    whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
            except Exception:
                text = font.render("Something went wrong :/", True, (255, 0, 255))
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HIGHT//2))
                pygame.display.update()
                sleep(4)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # checking if 1 is pressed
                    pawn_to_get_moved = get_pawns_location(remote_chinczyk_board[str(player_order)])[0]
                    print(f"pawn_to_get_moved={pawn_to_get_moved}, dice_roll={dice_roll}")
                    resp = requests.get(BASE_URL + f"/game_move?client_id={player_id}&pawn_field={pawn_to_get_moved}&dice_roll={dice_roll}")
                    if dice_roll != 6:
                        whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
                    dice_roll = -1
                elif event.key == pygame.K_2: # checking if 2 is pressed
                    pawn_to_get_moved = get_pawns_location(remote_chinczyk_board[str(player_order)])[1]
                    resp = requests.get(BASE_URL + f"/game_move?client_id={player_id}&pawn_field={pawn_to_get_moved}&dice_roll={dice_roll}")
                    if dice_roll != 6:
                        whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
                    dice_roll = -1
                elif event.key == pygame.K_3: # checking if 3 is pressed
                    pawn_to_get_moved = get_pawns_location(remote_chinczyk_board[str(player_order)])[2]
                    resp = requests.get(BASE_URL + f"/game_move?client_id={player_id}&pawn_field={pawn_to_get_moved}&dice_roll={dice_roll}")
                    if dice_roll != 6:
                        whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
                    dice_roll = -1
                elif event.key == pygame.K_4: # checking if 4 is pressed
                    pawn_to_get_moved = get_pawns_location(remote_chinczyk_board[str(player_order)])[3]
                    resp = requests.get(BASE_URL + f"/game_move?client_id={player_id}&pawn_field={pawn_to_get_moved}&dice_roll={dice_roll}")
                    if dice_roll != 6:
                        whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
                    dice_roll = -1
                elif event.key == pygame.K_s: # pressing s == skip
                    resp = requests.get(BASE_URL + f"/skip_turn?client_id={player_id}")
                    whos_turn_is_it = (whos_turn_is_it+1)%number_of_players
            elif event.type == pygame.QUIT:
                run = False
                action_was_taken = True 
    
    while waiting_for_players_to_join:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        screen.fill((0, 0, 0))
        text = font.render("Waiting for other players to join...", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HIGHT//2))
        pygame.display.update()
        resp = requests.get(BASE_URL + "/game_turn")
        if resp.status_code == 200:
            waiting_for_players_to_join = False
            whos_turn_is_it = resp.json()['message']
            break

    # leaving the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
