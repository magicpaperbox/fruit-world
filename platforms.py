import pygame


class Platform:
    def __init__(self, width: float, height: float, x: float, y: float):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 100))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surface, self.rect)