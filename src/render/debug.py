import pygame

from screen.fonts import FontsFactory, FontSize, FontStyle
from screen.game_units import GameUnit

_debug_font: pygame.font.Font | None = None


def _get_debug_font() -> pygame.font.Font:
    global _debug_font
    if _debug_font is None:
        _debug_font = FontsFactory().get_font(FontSize.LARGE, FontStyle.SIMPLE)
    return _debug_font


def draw_rect(
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple[int, int, int],
    label: str = "RECT",
    alpha: int = 50,
    border_width: int = GameUnit(2).non_zero_pixels,
    show_anchors: bool = True,
):
    font = _get_debug_font()
    r, g, b = color

    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((r, g, b, max(0, min(alpha, 255))))
    screen.blit(overlay, rect.topleft)
    pygame.draw.rect(screen, color, rect, width=border_width)
    label = font.render(label, True, color)
    screen.blit(label, (rect.x + GameUnit(4).non_zero_pixels, rect.y + GameUnit(4).non_zero_pixels))

    if show_anchors:
        pygame.draw.circle(screen, color, rect.center, GameUnit(2).non_zero_pixels)  # middle
        pygame.draw.circle(screen, color, rect.midbottom, GameUnit(3).non_zero_pixels)  # „feet”


def draw_area(
    screen: pygame.Surface,
    items_to_draw: list,
    color: tuple[int, int, int],
    label: str = "RECT",
    alpha: int = 80,
    border_width: int = GameUnit(2).non_zero_pixels,
    show_anchors: bool = False,
):
    for index, item in enumerate(items_to_draw, start=1):
        rect = item.rect
        item_label = f"{label} {index}"
        draw_rect(
            screen=screen,
            rect=rect,
            color=color,
            label=item_label,
            alpha=alpha,
            border_width=border_width,
            show_anchors=show_anchors,
        )
