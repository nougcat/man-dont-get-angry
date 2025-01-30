# man-dont-get-angry

game of chińczyk (Man, Don't Get Angry)

instalacja potrzebnych pakietów
```sh
pip requirements.txt -r

```

Uruchamiamy serwer:
```sh

python3 server.py
```


```sh
# domyślnie PORT to 2137
localhost:PORT/game_init?how_many_players=2
```

```sh
python3 client.py
```

my thoughts on this project:
- I have learned fastapi, even though it's propably styled not in a good way i learned a lot and next time i will write it better
- I despise pygame
- I made a recap of bash function, but also what's not visible - i used [unix pipes](https://en.wikipedia.org/wiki/Pipeline_(Unix)) to get rid of useless garbadge that fastapi is showing me, and i focused on warnings, errors and info logs

overall this project was PITA, but i learned a lot