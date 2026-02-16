import math
import random

import pygame
from pygame import Vector2

from render.sprite_factory import SPRITE_FACTORY
from screen.game_units import RelativeUnit


class Particle:
    def __init__(self, position: tuple[int, int], direction: Vector2, speed: float, lifetime_ms: int = 500):
        self._position = Vector2(position)  # 2D vector
        self._direction = direction
        self._speed = speed
        self._lifetime_ms = lifetime_ms
        self._initial_lifetime = lifetime_ms

        icon_height = RelativeUnit(0.03).pixels_y
        self._image = SPRITE_FACTORY.load("sprites/items/spark.png", icon_height)
        self._original_image = self._image

    def update(self, dt: int):
        self._lifetime_ms -= dt
        self._position += self._direction * self._speed * dt

    def is_alive(self) -> bool:
        return self._lifetime_ms > 0

    def draw_fadeout(self, screen: pygame.Surface):
        _alpha = int(255 * (self._lifetime_ms / self._initial_lifetime))
        _alpha = max(0, min(255, _alpha))
        # Create more transparent copy
        _image_copy = self._image.copy()
        _image_copy.set_alpha(_alpha)
        screen.blit(_image_copy, self._position)

    def draw_blink(self, screen: pygame.Surface):
        _scale = max(0.3, (self._lifetime_ms / self._initial_lifetime))
        _new_width = int(self._original_image.get_width() * _scale)
        _new_height = int(self._original_image.get_height() * _scale)

        if _new_width > 0 and _new_height > 0:
            _scaled_image = pygame.transform.scale(self._original_image, (_new_width, _new_height))
            screen.blit(_scaled_image, self._position)
        else:
            screen.blit(self._image, self._position)

    @staticmethod
    def spawn_particles(pos: tuple[int, int]) -> list["Particle"]:
        particle_amount = 80
        particles = []
        for i in range(particle_amount):
            angle = random.uniform(0, 2 * 3.14159)  # rad
            direction = Vector2(math.cos(angle), math.sin(angle))
            speed = random.uniform(0.05, 0.15)
            particle = Particle(pos, direction, speed)
            particles.append(particle)
        return particles

    @staticmethod
    def create_blink_effect(screen: pygame.Surface, particles: list, dt: int) -> list["Particle"]:
        for particle in particles:
            particle.update(dt)
            particle.draw_blink(screen)
        particles = [p for p in particles if p.is_alive()]
        return particles
