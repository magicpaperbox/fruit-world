from enum import Enum, auto


class Action(Enum):
    NONE = auto()
    CLOSE_MENU = auto()
    QUIT_GAME = auto()
    RESET_LEVEL = auto()
    RES_800x600 = auto()
    RES_1280x720 = auto()
    START_GAME = auto()
    GO_TO_MENU = auto()
    CLOSE_WINDOW = auto()
    OPEN_SETTINGS_IN_MAIN_MENU = auto()
