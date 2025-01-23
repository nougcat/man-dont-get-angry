import pygame
from first_run import first_run
from time import sleep
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HIGHT = 800


BASE_URL="http://localhost:2137"
import requests
import random

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

run = True
first_run_bool = True
game_not_active = True
whos_turn_is_it = -1
player_order = -1

def draw_player_base(pygame, screen, player_color, square_size, x_start, y_start):
    for row in range(2):
        for col in range(2):
            x = x_start + col * square_size
            y = y_start + row * square_size
            pygame.draw.rect(screen, player_color, (x, y, square_size, square_size))

font = pygame.font.Font(None, 36)
while run:
    # making blank screen
    screen.fill((0, 0, 0))
    if first_run_bool:
        (player_id, player_order, number_of_players) = first_run()
        first_run_bool = False
        chinczyk_board = [
            [0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 8, 8, 8, 8, 0, 4, 4, 4, 4, 1],
            [9, 1, 1, 1, 1, 6, 1, 1, 1, 1, 5],
            [0, 0, 0, 0, 1, 6, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 6, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 6, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 7, 1, 1, 0, 0, 0, 0]
        ]

    # Drawing a chessboard
    square_size = 40
    for row in range(11):
        for col in range(11):
            if chinczyk_board[row][col]:
                x = col * square_size + (SCREEN_WIDTH - 400) // 2
                y = row * square_size + (SCREEN_HIGHT - 400) // 2
                if chinczyk_board[row][col] == 2:
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 3:
                    pygame.draw.rect(screen, (128, 0, 0), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 4:
                    pygame.draw.rect(screen, (0, 255, 0), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 5:
                    pygame.draw.rect(screen, (0, 128, 0), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 6 and number_of_players > 2:
                    pygame.draw.rect(screen, (0, 0, 255), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 7 and number_of_players > 2:
                    pygame.draw.rect(screen, (0, 0, 128), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 8 and number_of_players > 3:
                    pygame.draw.rect(screen, (255, 255, 0), (x, y, square_size, square_size))
                elif chinczyk_board[row][col] == 9 and number_of_players > 3:
                    pygame.draw.rect(screen, (128, 128, 0), (x, y, square_size, square_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, square_size, square_size))
    # drawing corners (players)
    player_color_1 = (255, 0, 0)
    draw_player_base(pygame, screen, player_color_1, square_size, 0, 0)
    player_color_2 = (0, 255, 0)
    draw_player_base(pygame, screen, player_color_2, square_size, 0, SCREEN_HIGHT - 2 * square_size)
    if number_of_players > 2:
        player_color_3 = (0, 0, 255)
        draw_player_base(pygame, screen, player_color_3, square_size, SCREEN_HIGHT - 2 * square_size, 0)
        if number_of_players > 3:
            player_color_4 = (255, 255, 0)
            draw_player_base(pygame, screen, player_color_4, square_size, SCREEN_WIDTH - 2 * square_size,
                             SCREEN_HIGHT - 2 * square_size)

    # displaying pawns
    


    if player_order == whos_turn_is_it:
        dice_roll = random.randint(1, 6)
        dice_text = font.render(f"You've rolled: {dice_roll}", True, (255, 255, 255))
        screen.blit(dice_text, (SCREEN_WIDTH//2 - dice_text.get_width()//2, 50))
        pygame.display.update()
    while player_order == whos_turn_is_it and not game_not_active:
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # move first pawn 
                    pass
                if event.button == 2:
                    # move second pawn
                    pass
                if event.button == 3:
                    # move third pawn
                    pass
                if event.button == 4:
                    # move fourth pawn
                    pass
                if event.type == pygame.QUIT:
                    run = False
                    break
        sleep(0.3)
    
    while player_order != whos_turn_is_it and not game_not_active:
        text = font.render("Waiting for other player turn...", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 10))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        sleep(0.3)
        resp = requests.get(BASE_URL + "/game_turn")
        try:
            if resp['message'] != whos_turn_is_it:
                whos_turn_is_it = resp['message']
        except Exception:
            pass
    
    while game_not_active:
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
            game_not_active = False
            whos_turn_is_it = resp.json()['message']
            break
        
        sleep(0.1)
    
    # freeze everything unless game is active
    for event in pygame.event.get():
        # X to wyjście z gry
        if event.type == pygame.QUIT:
            run = False    

pygame.quit()
