import pygame


def draw_rect(
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple[int, int, int],
    label: str = "RECT",
    alpha: int = 50,
    border_width: int = 2,
    show_anchors: bool = True,
):
    font = pygame.font.SysFont("comicsansms", 9)
    r, g, b = color

    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((r, g, b, max(0, min(alpha, 255))))
    screen.blit(overlay, rect.topleft)
    # obrys
    pygame.draw.rect(screen, color, rect, width=border_width)
    # etykieta
    label = font.render(label, True, color)
    screen.blit(label, (rect.x + 4, rect.y + 4))

    if show_anchors:
        pygame.draw.circle(screen, color, rect.center, 2)  # środek
        pygame.draw.circle(screen, color, rect.midbottom, 3)  # „stopy”


def draw_area(
    screen: pygame.Surface,
    items_to_draw: list,
    color: tuple[int, int, int],
    label: str = "RECT",
    alpha: int = 80,
    border_width: int = 2,
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
