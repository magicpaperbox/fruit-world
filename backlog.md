draw_bush_debug
- zunifikować sposób rysowania wszystkich prostokątów debugowych
- brak typów

dialog_box - rozdzielić logikę wyświetlania tekstu w okienku od logiki rozmowy z npc

przejść z scale_screen.GAME_HEIGHT na GAME_HEIGHT

GAME_HEIGHT jest przypisywane do SCREEN_HEIGHT -> użyć GAME_HEIGHT bezpośrednio
to samo GAME_WIDTH

StaticObject powinien używać pozycji top left corner a nie center