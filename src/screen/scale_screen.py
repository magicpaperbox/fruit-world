import pygame

_RES_360p = 640, 360
_RES_720p = 1280, 720
_RES_HD = 1600, 900
_RES_1080p = 1920, 1080
_RES_2K = 2048, 1152

_AVAILABLE_RESOLUTIONS = [
    _RES_360p,
    _RES_720p,
    _RES_HD,
    _RES_1080p,
    _RES_2K,
]

_GUI_HEIGHT_RATIO = 0.1
# _chosen_size = RES_HD
_chosen_res = _AVAILABLE_RESOLUTIONS[1]

_SIDE_PANEL_RATIO = 0.140625
SCREEN_WIDTH, SCREEN_HEIGHT = _chosen_res
SIDE_PANEL_W = None
DIALOG_HEIGHT = None
GAME_WIDTH: int | None = None
GAME_HEIGHT: int | None = None

_CANONICAL_SCREEN_HEIGHT = 1080


def get_font_size():
    if _chosen_res == _AVAILABLE_RESOLUTIONS[0]:
        size = 10
    elif _chosen_res == _AVAILABLE_RESOLUTIONS[1]:
        size = 12
    elif _chosen_res == _AVAILABLE_RESOLUTIONS[2]:
        size = 14
    else:
        size = 18
    return size


def recalc_sizes(width: int, height: int):
    global SCREEN_WIDTH, SCREEN_HEIGHT, GAME_WIDTH, GAME_HEIGHT, DIALOG_HEIGHT, SIDE_PANEL_W

    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

    DIALOG_HEIGHT = int(_GUI_HEIGHT_RATIO * SCREEN_HEIGHT)
    SIDE_PANEL_W = int(SCREEN_WIDTH * _SIDE_PANEL_RATIO)
    GAME_WIDTH = SCREEN_WIDTH - SIDE_PANEL_W
    GAME_HEIGHT = SCREEN_HEIGHT


def init_display(width: int, height: int, fullscreen: bool):
    recalc_sizes(width, height)

    flags = pygame.FULLSCREEN if fullscreen else 0
    return pygame.display.set_mode((width, height), flags)


def game_units_to_px(units: int) -> int:  # Skalowanie stałych jednostek gry na piksele
    return int(units * SCREEN_HEIGHT / _CANONICAL_SCREEN_HEIGHT)


def game_units_to_decimal(units: float) -> float:  # Skalowanie stałych jednostek gry na piksele
    return units * SCREEN_HEIGHT / _CANONICAL_SCREEN_HEIGHT


def relative_x_to_game_units_px(horizontal_pos: float) -> int:  # zachowanie proporcji świata niezależnie od okna
    return int(horizontal_pos * GAME_WIDTH)


def relative_y_to_game_units_px(vertical_pos: float) -> int:
    return int(vertical_pos * GAME_HEIGHT)


def relative_coords_to_game_units_px(horizontal_pos: float, vertical_pos: float) -> tuple[int, int]:
    return int(horizontal_pos * GAME_WIDTH), int(vertical_pos * GAME_HEIGHT)


def relative_x_to_screen_units(horizontal_pos: float) -> int:
    return int(horizontal_pos * SCREEN_WIDTH)


def relative_y_to_screen_units(vertical_pos: float) -> int:
    return int(vertical_pos * SCREEN_HEIGHT)
