import pygame
from render.sprite_factory import SPRITE_FACTORY
from screen import scale_screen as ss


# class Platform:
#     def __init__(self, x: float, y: float, platform: str):
#         height = ss.relative_y_to_game_units_px(0.2)
#         platform_sprite = SPRITE_FACTORY.load(f"sprites/objects/{platform}.png", height)
#         self.width = platform_sprite.get_width()
#         self.height = platform_sprite.get_height()
#         self.rect = pygame.rect.Rect(x, y, self.width, self.height)
#         self.surface = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
#
#
#     def create_puzzle_platform(self, segments: int, join_left: bool, join_right: bool):
#         pass
#
# #to bedzie musialo sie sklejac w platforme ale dane sie poda dla levela a nie tu wiec x i y sa tu roboczo
#         # middle_platform = Platform(400, 500, "grass_ground_center")
#         # left_platform = Platform(700, 600, "grass_ground_left")
#         # right_platform = Platform(700, 600, "grass_ground_right")
#
#     def draw(self, screen: pygame.surface.Surface):
#         screen.blit(self.surface, self.rect)
#
#     def __str__(self):
#         return f"left: {self.rect.left}, right: {self.rect.right}, top: {self.rect.top}, bottom: {self.rect.bottom}"
#



# #to bedzie w levelu czyli w tym object spec chyba
# small_platform = Platform(400, 500, "platform_small")
# big_platform = Platform(700, 600, "platform_wide")
#
# small_platform.surface.fill((255, 0, 0, 0))
# big_platform.surface.fill((255, 0, 0, 0))


# class Platform:
#     def __init__(self, x: float, y: float, width: float, height: float):
#         self.rect = pygame.rect.Rect(x, y, width, height)
#         self.surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
#         self.surface.fill((255, 0, 0, 0))
#
#     def draw(self, screen: pygame.surface.Surface):
#         screen.blit(self.surface, self.rect)
#
#     def __str__(self):
#         return f"left: {self.rect.left}, right: {self.rect.right}, top: {self.rect.top}, bottom: {self.rect.bottom}"


