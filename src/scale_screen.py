SIZE_360p = 640, 360
SIZE_720p = 1280, 720
SIZE_HD = 1600, 900
SIZE_1080p = 1920, 1080
SIZE_2K = 2048, 1152

_chosen_size = SIZE_720p

_GUI_HEIGHT_RATIO = 0.1
SCREEN_WIDTH, SCREEN_HEIGHT = _chosen_size
DIALOG_HEIGHT = int(_GUI_HEIGHT_RATIO * SCREEN_HEIGHT)
GAME_WIDTH = SCREEN_WIDTH - DIALOG_HEIGHT * 4
GAME_HEIGHT = SCREEN_HEIGHT - DIALOG_HEIGHT

_CANONICAL_SCREEN_HEIGHT = 1080

def game_units_to_px(units: int) -> int: #Skalowanie stałych jednostek gry na piksele
    return int(units * SCREEN_HEIGHT / _CANONICAL_SCREEN_HEIGHT)

def game_units_to_decimal(units: float) -> float: #Skalowanie stałych jednostek gry na piksele
    return units * SCREEN_HEIGHT / _CANONICAL_SCREEN_HEIGHT

def relative_x_to_game_units_px(horizontal_pos: float) -> int: #zachowanie proporcji świata niezależnie od okna
    return int(horizontal_pos * GAME_WIDTH)

def relative_y_to_game_units_px(vertical_pos: float) -> int:
    return int(vertical_pos * GAME_HEIGHT)

def relative_coords_to_game_units_px(horizontal_pos: float, vertical_pos: float) -> tuple[int, int]:
    return int(horizontal_pos * GAME_WIDTH), int(vertical_pos * GAME_HEIGHT)
