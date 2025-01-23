import pygame
import json
import requests
from time import sleep
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HIGHT = 800
BASE_URL="http://localhost:2137"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
main_active = True
server_in_init_state = True
user_input = ""
notification_txt = "Enter number of players:"

try:
    while main_active:
        screen.fill((0, 0, 0))
        # Create font object
        font = pygame.font.Font(None, 36)
        # Initialize input variables
        if server_in_init_state:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            inp = int(user_input)
                            if inp < 2 or inp > 4:
                                user_input = ""
                                notification_txt = "Number of players must be between 2 and 4"
                            else:
                                number_of_players = int(user_input)
                                # nr. of players
                                URL = BASE_URL + f"/game_init?how_many_players={number_of_players}"
                                resp = requests.get(URL)
                                notification_txt = "If all players connected press A to start the game sever:"
                                sleep(1)
                                user_input = ""
                                server_in_init_state= False
                                
                        except ValueError:
                            user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
                if event.type == pygame.QUIT:
                    main_active = False
                    # make a code that will the game exit

        if not server_in_init_state:
            url = BASE_URL + f"/game_list_users"
            players_dict = requests.get(url).json()
            players_joined = font.render("avalible players:"+str(len(players_dict))+f"/{number_of_players}", True, (255, 0, 0))
            screen.blit(players_joined, (SCREEN_HIGHT/2, SCREEN_WIDTH/2))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            inp = (user_input).strip().lower()
                            if inp[0] != 'a':
                                user_input = ""
                                notification_txt = (
                                    "That's not valid input. Press A to activate sever"
                                )
                            else:
                                url = BASE_URL + "/game_start"
                                resp = requests.get(url).json()
                                try:
                                    if resp['message'] == "Success":
                                        main_active == False
                                    else:
                                        notification_txt = "Not all players have joined"
                                        user_input = ""
                                except Exception:
                                    notification_txt = "unknown error"
                                    user_input = ""

                            
                        except ValueError:
                            user_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
                if event.type == pygame.QUIT:
                    server_in_init_state = False
                    # make a code that will the game exit

        # rendering input rectangle
        input_rect = pygame.Rect(300, 100, 140, 32)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        # rendering notification
        notification = font.render(notification_txt, True, (255, 0, 0))
        screen.blit(notification, (200 - len(notification_txt), 50))
        # rendering the input
        txt_surface = font.render(user_input, True, (255, 255, 255))
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()
except requests.exceptions.ConnectionError:
    print("ERROR: sever not active")