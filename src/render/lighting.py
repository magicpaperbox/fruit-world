import pygame

from screen.game_units import GameUnit


class Lighting:
    def __init__(self, width: int, height: int):
        self._size = (width, height)
        self._ambient_color = (210, 215, 230)
        self._light_surface = pygame.Surface(self._size)
        self._light_texture = self._generate_light_texture(radius=GameUnit(120).pixels)

    @staticmethod
    def _generate_light_texture(radius: int) -> pygame.Surface:
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        for r in range(radius, 0, -5):
            # Im bliżej środka, tym jaśniej (alpha jest mała, ale nakładamy wiele warstw)
            alpha = 100
            pygame.draw.circle(surf, (255, 255, 255, alpha), (radius, radius), r)
        return surf

    def reset(self):
        self._light_surface.fill(self._ambient_color)

    def draw_light(self, center_pos: tuple[int, int]):
        # Rysujemy światło na warstwie mroku
        # Używamy BLEND_ADD, żeby "dodać jasność" do mroku
        x, y = center_pos
        # radius = self.light_texture.get_width() // 2
        dest_rect = self._light_texture.get_rect(center=(x, y))
        self._light_surface.blit(self._light_texture, dest_rect, special_flags=pygame.BLEND_ADD)

    def apply(self, target_surface: pygame.Surface):
        # BLEND_MULT sprawia, że to, co ciemne na mapie, przyciemnia grę.
        target_surface.blit(self._light_surface, (0, 0), special_flags=pygame.BLEND_MULT)


class SunLight:
    def __init__(self):
        self.time = 0.0
        # Kolor: Przy BLEND_ADD (dodawaniu) czerń (0,0,0) to brak zmian.
        self.base_color = (40, 20, 0)
        self.ray_texture = self._generate_ray_texture(GameUnit(500).pixels, GameUnit(2000).pixels)

    def _generate_ray_texture(self, width: int, height: int) -> pygame.Surface:
        surf = pygame.Surface((width, height))
        surf.fill((0, 0, 0))  # Tło czarne (nie doda nic do obrazu)
        # Środek promienia jest jasny, boki wygasają do czerni
        center_x = width / 2.0
        for x in range(width):
            # Odległość od środka (0,0 w środku, 1,0 na krawędzi)
            dist = abs(x - center_x) / center_x
            intensity = max(0.0, 1 - dist * dist)

            # Obliczamy kolor paska
            r = int(self.base_color[0] * intensity)
            g = int(self.base_color[1] * intensity)
            b = int(self.base_color[2] * intensity)

            pygame.draw.line(surf, (r, g, b), (x, 0), (x, height))
        return pygame.transform.rotozoom(surf, GameUnit(-20).pixels, 1.0)

    def update(self, dt):
        self.time += dt * 0.0005

    def draw(self, screen: pygame.Surface):
        sw, sh = screen.get_size()
        num_rays = 6
        gap = sw / (num_rays - 1) * 1.3

        for i in range(num_rays):
            # Każdy promień rusza się trochę inaczej
            speed_mult = 1.0 + ((i % 3) * 0.2)
            # modulo (sw + 800), żeby promienie wyjeżdżały i wjeżdżały płynnie
            # 800 to margines na szerokość obróconego promienia
            total_w = sw + GameUnit(900).pixels
            base_x = (self.time * GameUnit(50).pixels * speed_mult + i * gap) % total_w
            x = base_x - GameUnit(400).pixels  # Cofamy o margines
            y = GameUnit(-500).pixels

            screen.blit(self.ray_texture, (x, y), special_flags=pygame.BLEND_ADD)
