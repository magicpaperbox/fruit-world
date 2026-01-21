# Task 1
w npc została logika cache spriteów - zmigrować na SPRITE_FACTORY ✅

# Task 2
Zmigrować static_objects z LevelSpec na SpriteObjectSpec ✅

# Task 3
Do zastanowienia: Zmigrować bushes na SpriteObjectSpec ✅

# Task 4
Przenieść wszystkie latające platformy z old_platforms do platforms

# Task 5
Zaimplementować PuzzlePlatform -> Bardziej złożony SpriteObject

class DynamicSpriteObjectSpec:
  x: int
  y: int
  height: int # game units
  segments_count: int
  center_sprite_path: str
  left_sprite_path: str | None = None
  right_sprite_path: str | None = None

class DynamicSpriteObject:
  rect: Rect

  def draw(self, screen: pygame.surface.Surface):
    pass
  
  def __init__(???):
    pass