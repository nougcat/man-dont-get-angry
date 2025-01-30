from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import json

app = FastAPI()

app.users_list = []
colors = ["red", "blue", "green", "yellow"]

app.how_many_players = 0

app.is_game_started = 0
app.whos_turn_is_it = -1  # -1 = noone's, 0 = red, 1 = blue, etc.


@app.get("/")
async def root():
    return {"message": "hello world, this page does nothing"}


@app.get("/game_init")
async def game_init(how_many_players: int):
    if app.how_many_players != 0:
        raise HTTPException(status_code=403, detail="Game has already initialized")
    elif 4 >= how_many_players >= 2:
        app.users_list = []
        app.how_many_players = how_many_players
        return {"message": "Success"}
    else:
        raise HTTPException(status_code=400, detail="invalid number of players")


@app.get("/game_max_users")
async def game_max_users():
    return {"message": app.how_many_players}

@app.get("/game_join")
async def game_join(client_id: int):
    if app.is_game_started:
        raise HTTPException(status_code=403, detail="Game has started already")
    elif (client_id not in app.users_list) and len(app.users_list)+1 <= app.how_many_players:
        app.users_list.append(client_id)
        if len(app.users_list) == app.how_many_players:
            await start_game()
        return {"message": app.users_list.index(client_id)}  # returning the player turn
    elif client_id in app.users_list:
        raise HTTPException(status_code=400, detail="user is already here")
    elif len(app.users_list)+1 >= app.how_many_players:
        raise HTTPException(status_code=400, detail="too many players")
    else:
        raise HTTPException(status_code=500, detail="unknown error")  # http://http.cat/500

@app.get("/game_list_users")
async def game_list_users():
    return JSONResponse(app.users_list)


@app.get("/game_start")
async def start_game():
    if len(app.users_list) != app.how_many_players:
        raise HTTPException(status_code=403, detail="invalid number of players")
    else:
        logger.info("Game has started")
        app.board = [[] for x in range(app.how_many_players)]
        for x in range(app.how_many_players):
            app.board[x] = [0 for y in range(75)]
            app.board[x][74] = 4  # pionki których nie ma na planszy

        app.is_game_started = 1
        app.whos_turn_is_it = 0
        return {"message": "Success"}


# ignore_user == user_who_called_this_function, field must be between 0 to 69
async def remove_pawns(ignore_user: int, dice_roll: int):
    if dice_roll >= 70:
        return None #can't beat any pawns if index is over 69
    for x in range(app.how_many_players):
        if x == ignore_user:
            continue  # we skip current user's pawns
        if dice_roll >= 40:
            dice_roll -= 40  # field 40 is the same as 0

        if dice_roll <= 30:
            if app.board[x][dice_roll] > 0:
                app.board[x][74] += app.board[x][dice_roll]  # removing the pawn from the board
                app.board[x][dice_roll] = 0
            if app.board[x][dice_roll + 40] > 0:
                app.board[x][74] += app.board[x][dice_roll + 40]  # removing the pawn from the board
                app.board[x][dice_roll + 40] = 0
        else:  # field here is between 31 and 39
            if app.board[x][dice_roll] > 0:
                app.board[x][74] += app.board[x][dice_roll]  # removing the pawn from the board
                app.board[x][dice_roll] = 0


# pawn_field == field on which pawn is located
@app.get("/game_move")
async def movement(client_id: int, pawn_field: int, dice_roll: int):
    logger.warning(f'client_id={client_id}, pawn_field={pawn_field}, dice_roll={dice_roll}')
    # checking if it's user turn
    try:
        if app.whos_turn_is_it == app.users_list.index(client_id):
            index_of_user = app.users_list.index(client_id)
        else:
            logger.info("It's turn of user: " + str(app.whos_turn_is_it))
            raise HTTPException(status_code=403, detail="It's not your turn")
    except ValueError:
        raise HTTPException(status_code=401, detail="There is no such a user")

    # game logic
    try:
        if app.board[index_of_user][pawn_field]:
            if pawn_field == 74 and dice_roll in {0,6}:  # adding pawn to the board
                app.board[index_of_user][pawn_field] -= 1  # removing old pawn
                dice_roll = 0
                pawn_field = 0 + 10 * index_of_user  # we add this number because diffrent players have different starting tile
                await remove_pawns(index_of_user, pawn_field)  # removing pawns of other players
                app.board[index_of_user][pawn_field + dice_roll] += 1  # adding pawn in new place
                return {"message": "Success"}

            if (pawn_field + dice_roll > 43 + index_of_user * 10 and pawn_field < 70) or pawn_field+dice_roll>73:
                # checking if pawn is out of range (out of board)
                logger.warning(f'pawn_field={pawn_field}, dice_roll={dice_roll}, index_of_user={index_of_user}')
                await next_turn(client_id)
                return {"message": "Success"}  # next rolling a dice is not possible

            # checking if the place where pawn lands is on the board
            if pawn_field + dice_roll < 40 + index_of_user * 10:
                await remove_pawns(index_of_user, pawn_field + dice_roll)
                app.board[index_of_user][pawn_field] -= 1
                app.board[index_of_user][pawn_field + dice_roll] += 1
            elif 73 <= pawn_field + dice_roll + index_of_user * 10 >= 70 :  # if destination field is 70-73
                app.board[index_of_user][pawn_field] -= 1
                app.board[index_of_user][pawn_field + dice_roll] += 1
            elif 43 + index_of_user * 10 >= pawn_field + dice_roll >= 40 + index_of_user * 10 :  # if destination field is 40-43
                app.board[index_of_user][pawn_field] -= 1
                app.board[index_of_user][pawn_field + dice_roll + (3 - index_of_user) * 10] += 1

            

            # it's next turn unless you rolled 6 on a dice (0 is also 6)
            if not dice_roll in {0,6}:
                await next_turn(client_id)

            return {"message": "Success"}
        else:
            logger.info("There is no such a pawn")
            raise HTTPException(status_code=403, detail="there is no such a pawn")
    except ValueError:
        raise HTTPException(status_code=403, detail="there is no such a pawn")


# we need skip turn in case you roll something other than six, and all your pawns are at base
@app.get("/skip_turn")
async def next_turn(client_id: int):
    try:
        if app.whos_turn_is_it == app.users_list.index(client_id):
            app.whos_turn_is_it = (app.whos_turn_is_it + 1) % (app.how_many_players)
            return {"message": "Success"}
        else:
            raise HTTPException(status_code=403, detail="It's not your turn")
    except ValueError:
        raise HTTPException(status_code=401, detail="There is no such a user")


@app.get("/game_board")
async def game_board():
    if not app.is_game_started:
        raise HTTPException(status_code=403, detail="Game has not started")
    dict_out = {}
    for x in range(app.how_many_players):
        dict_out.setdefault(x, app.board[x])
    board_response = json.dumps(dict_out)
    return JSONResponse(content=board_response)


# returning who's turn is it
@app.get("/game_turn")
async def whos_turn():
    if not app.is_game_started:
        raise HTTPException(status_code=403, detail="Game has not started")
    return {"message": app.whos_turn_is_it}


@app.get("/game_won")
async def game_is_won():
    if not app.is_game_started:
        raise HTTPException(status_code=403, detail="Game has not started")
    for x in range(app.how_many_players):
        if app.board[x][73] == 4:
            return {"message": x}

    return {"message": -1}


@app.get("give_btc")
async def give_btc():
    raise HTTPException(status_code=418, detail="I'm teapot")  # http://http.cat/418



if __name__ == "__main__":
    # logging stuff
    import logging

    logger = logging.getLogger('uvicorn.error')
    fileHandler = logging.FileHandler("my_log.log")
    consoleHandler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
        fileHandler,
        consoleHandler
    ]
)
    
    uvicorn.run(app, host="localhost", port=2137)