import pygame


class Platform:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.surface = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 0, 0, 0))

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surface, self.rect)

    def __str__(self):
        return f"left: {self.rect.left}, right: {self.rect.right}, top: {self.rect.top}, bottom: {self.rect.bottom}"