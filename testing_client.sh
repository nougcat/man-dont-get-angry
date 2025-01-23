#!/bin/sh
BASE_URL="localhost:2137"

# init game
curl "${BASE_URL}/game_init?how_many_players=2"


# dołącz do serwera klientami teraz

echo "\nkliknij cokolwiek aby uruchomić serwer\n"

read n

curl "${BASE_URL}/game_start"