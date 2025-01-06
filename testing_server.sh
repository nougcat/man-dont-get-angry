#!/bin/sh
BASE_URL="localhost:2137"

# init game
curl "${BASE_URL}/game_init?how_many_players=3"

FIRST_PLAYER="535"
SECOND_PLAYER="536"
THIRD_PLAYER="537"
# joining game
curl "${BASE_URL}/game_join?client_id=${FIRST_PLAYER}"

curl "${BASE_URL}/game_join?client_id=${SECOND_PLAYER}"
curl "${BASE_URL}/game_join?client_id=${THIRD_PLAYER}"

# listing users
echo '\n'
curl "${BASE_URL}/game_list_users"


# starting game
curl "${BASE_URL}/game_start"
echo '\n'

echo "\nkliknij cokolwiek aby rozpocząć\n"
read something

curl "${BASE_URL}/game_move?client_id=${FIRST_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${FIRST_PLAYER}&pawn_field=0&steps_int=11" # to nie powinno być możliwe, ale robimy to aby testować czy możliwe jest zbicie pionka

echo '\n'
curl "${BASE_URL}/game_get_board"

curl "${BASE_URL}/game_move?client_id=${SECOND_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${SECOND_PLAYER}&pawn_field=10&steps_int=1" # zbijamy pionek gracza 1

echo '\n'
curl "${BASE_URL}/game_get_board"

echo "\nkliknij cokolwiek aby skończyć grę\n"
read something

curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=20&steps_int=43" # ruszamy się o 44 pola, czyli dokładie tyle aby wygrać
echo '\n'
curl "${BASE_URL}/game_get_board"
echo '\n'

curl "${BASE_URL}/skip_turn?client_id=${FIRST_PLAYER}"
curl "${BASE_URL}/skip_turn?client_id=${SECOND_PLAYER}"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=20&steps_int=43"

echo '\n'
curl "${BASE_URL}/game_get_board"
echo '\n'

curl "${BASE_URL}/skip_turn?client_id=${FIRST_PLAYER}"
curl "${BASE_URL}/skip_turn?client_id=${SECOND_PLAYER}"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=20&steps_int=43"

echo '\n'
curl "${BASE_URL}/game_get_board"
echo '\n'

curl "${BASE_URL}/skip_turn?client_id=${FIRST_PLAYER}"
curl "${BASE_URL}/skip_turn?client_id=${SECOND_PLAYER}"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=74&steps_int=6"
curl "${BASE_URL}/game_move?client_id=${THIRD_PLAYER}&pawn_field=20&steps_int=43"

echo '\n'
curl "${BASE_URL}/game_get_board"
echo '\n'

curl "${BASE_URL}/game_is_won"

