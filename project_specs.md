# spec servera:
plansza ma 40 pól na których może być użytkownik, ALE; jako że tych graczy jest 4, fajnie by było aby pionek nie przechodził z LIST_MAX na LIST_INDEX=0; to najsensowniejszym pomysłem jest zrobienie 80 pól.

- czerwony porusza się od 0 do 39; 70-73 pola na których nie może być zbity
- niebieski porusza się od 10 do 49; 70-73 pola na których nie może być zbity
- zielony porusza się od 20 do 59; 70-73 pola na których nie może być zbity
- żółty porusza się od 30 do 69; 70-73 pola na których nie może być zbity

jak widać, można zbić kogoś pionek na pozycji (X, X%40, albo X+40), trzeba sprawdzić wszystkie opcje, trzeba uważać by nie zrobić INDEX_OUT_OF_RANGE

pole nr. 73 to pole w którym są wygrane pionki, trzeba ich mieć 4

w indeksie nr. 74 są pionki których nie ma na planszy, czyli trzeba wyrzucić 6

# spec usera:
serwer wierzy, że użytkownik nie majstrował przy generatorze liczb losowych, oraz że na tyle na ile można - nie robi głupich requestów

poruszamy się pionkami klikając od 1-4, 1 oznacza pionek najbliżej mety, 4 najdalej

a 's' oznacza skip

# pomoce naukowa
- "Szybki jak FastAPI" Bill Lubanovic
- https://fastapi.tiangolo.com/
- https://pl.wikipedia.org/wiki/Chi%C5%84czyk_(gra_planszowa)
- https://www.pygame.org/docs/
