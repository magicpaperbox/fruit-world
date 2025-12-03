import pygame
from collisions import collision_x, collision_y
from platforms import Platform
import scale_screen
import player

SCREEN_WIDTH, SCREEN_HEIGHT = scale_screen.GAME_WIDTH, scale_screen.GAME_HEIGHT
target_height = scale_screen.target_height


class PlayerMobility:
    def __init__(self, gravity: float):
        self._gravity = gravity

        self._anchor = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.player_rect = pygame.Rect(0, 0, 45, target_height)  # do rysowania
        self.player_rect2 = pygame.Rect(0, 0, 45, 50)  # do kolizji w X
        self.player_rect3 = pygame.Rect(0, 0, 10, target_height)  # do kolizji w Y

        self._render_offset = 0
        self._belly_offset = -15
        self._legs_offset = 0

        self.player_velocity_y = 0
        self.jumps_left = 2
        self._on_ground = False

        self._sync_all()

    def _place_rect(self, rect: pygame.Rect, y_offset: int):
        ax, ay = self._anchor
        rect.midbottom = ax, ay + y_offset

    def _sync_all(self):
        self._place_rect(self.player_rect, self._render_offset)
        self._place_rect(self.player_rect2, self._belly_offset)
        self._place_rect(self.player_rect3, self._legs_offset)

    def _anchor_from_rect2(self):
        ax, ay = self.player_rect2.midbottom
        return ax, ay - self._belly_offset

    def _anchor_from_rect3(self):
        ax, ay = self.player_rect3.midbottom
        return ax, ay - self._legs_offset

    @property
    def is_on_ground(self):
        return self._on_ground

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.player_rect.x, self.player_rect.y

    def move_right(self, platforms: list[Platform]):
        self._move_horizontally(platforms, offset=2)

    def move_left(self, platforms: list[Platform]):
        self._move_horizontally(platforms, offset=-2)

    def _move_horizontally(self, platforms: list[Platform], offset: int):
        self.player_rect2.x += offset
        collision_x(platforms, self.player_rect2)
        self._anchor = self._anchor_from_rect2()
        self._sync_all()


    def move_vertically(self, platforms: list[Platform], dt: int):
        prev_top = self.player_rect3.top
        prev_bottom = self.player_rect3.bottom
        self.player_rect3.y += self.player_velocity_y * dt  # y
        self.player_velocity_y += self._gravity * dt  # dy
        player_velocity_y, on_ground = collision_y(platforms, self.player_rect3, self.player_velocity_y)
        self.player_velocity_y = player_velocity_y
        self._on_ground = on_ground
        self._anchor = self._anchor_from_rect3()
        self._sync_all()
        if self._on_ground:
            self.jumps_left = 2


    def jump(self):
        if self.jumps_left > 0:
            self.jumps_left -= 1
            self.player_velocity_y = -0.4
            self._on_ground = False


def draw_rect_debug(
    screen: pygame.Surface,
    font: pygame.font.Font,
    rect: pygame.Rect,
    color: tuple[int, int, int],
    label: str = "RECT",
    alpha: int = 50,
    border_width: int = 2,
    show_anchors: bool = True,
):
    """Rysuje półprzezroczyste wypełnienie, obrys i etykietę dla pojedynczego recta."""
    # półprzezroczyste wypełnienie
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    r, g, b = color
    overlay.fill((r, g, b, max(0, min(alpha, 255))))
    screen.blit(overlay, (rect.x, rect.y))

    # obrys
    pygame.draw.rect(screen, color, rect, width=border_width)

    # etykieta
    text = font.render(label, True, color)
    screen.blit(text, (rect.x + 4, rect.y + 4))

    if show_anchors:
        # środek
        pygame.draw.circle(screen, color, rect.center, 2)
        # „stopy” (midbottom)
        pygame.draw.circle(screen, color, rect.midbottom, 3)