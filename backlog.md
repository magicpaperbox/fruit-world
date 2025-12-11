# TASK-1
# Difficulty: 1
StaticObject powinien używać pozycji top left corner a nie center ✅

# TASK-2
# Difficulty: 2
draw_bush_debug
- zunifikować sposób rysowania wszystkich prostokątów debugowych ✅
- brak typów ✅

# TASK-3
# Difficulty: 3
unify loading and scaling sprite for item.py, map_loading.py, npcs.py, player.py static_objects.py
think of shared code that can be used everwhere consistently
```python
surface = SpriteManager.load("objects/domek.png", target_height=40) # the number should be in game units
```

# TASK-4
# Difficulty: 3
make sure sprite caching works for the SpriteManager - even if we ask for the same sprite 10 times it should only be loaded once
> ! Depends on TASK-3

# TASK-5
# Difficulty 2:
Make load_level return a Level object instead of large tuple so that main code can refer to platforms like this:
current_level.platforms

# TASK-6
# Difficulty 2:
Notice that Item, StaticObject and Platform and even Bush are all the same rectangles with or without sprites.
Their meaning is defined by which list in load_level they end up in.
Create a new class and replace existing variants. Name it StaticObject/GameObject/Object/???

# TASK-7
# Difficulty: 10
dialog_box - rozdzielić logikę wyświetlania tekstu w okienku od logiki rozmowy z npc
- separate rendering dialog selecting options, showing, hiding dialog etc. from npc logic using callbacks



