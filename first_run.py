def first_run():
    """
    this function sets your user id, and your player order
    """
    BASE_URL="http://localhost:2137"
    from random import random

    user_id = int(random() * 1000000)

    import requests

    resp = requests.get(BASE_URL + f"/game_join?client_id={user_id}")
    
    player_order = int(resp.json()['message'])

    resp_player_count = requests.get(BASE_URL + f"/game_max_users")
    player_count = int(resp_player_count.json()['message'])
    

    return (user_id, player_order, player_count)

