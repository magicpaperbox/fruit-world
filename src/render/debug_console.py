import enum

import pygame

from menu.ui import ColorTheme
from render.drawable import Drawable
from screen.game_units import GameUnit


class CommandType(str, enum.Enum):
    TELEPORT = "map"
    SPEEDUP = "speed"


class Command:
    def __init__(self, command_type: CommandType, data: str):
        self.command_type = command_type
        self.data = data


class DebugConsole(Drawable):
    def __init__(self, font: pygame.font.Font, theme: ColorTheme):
        self.is_opened = False
        self._input_text = ""

        self._theme = theme
        self._font = font
        self._rect = pygame.Rect(0, 0, GameUnit(500).pixels, GameUnit(100).pixels)
        self._border = GameUnit(3).non_zero_pixels
        self._border_radius = GameUnit(15).pixels

    def _do_task(self, command: Command):
        if command.command_type == CommandType.SPEEDUP:
            speedup = int(command.data) if command.data else 200
            self.player._mobility._velocity_x_px_per_sec += GameUnit(speedup).pixels

    def _parse_command(self, text: str) -> Command | None:
        text = text.strip()
        for command_type in CommandType:
            if text.startswith(command_type.value):
                data = text.removeprefix(command_type.value)
                return Command(command_type, data)
        return None

    def draw(self, screen: pygame.Surface):
        if not self.is_opened:
            return
        # TODO draw input text, handle errors with color
        pygame.draw.rect(screen, self._theme.modal_bg, self._rect, border_radius=GameUnit(35).pixels)
        # pygame.draw.rect(screen, self._theme.modal_border, self._rect, width=self._border, border_radius=GameUnit(15).pixels)
        # shadow_rect = self._rect.inflate(self._theme.modal_shadow, self._theme.modal_border).move(1, 1)
        # pygame.draw.rect(screen, self._theme.modal_shadow, shadow_rect, width=self._border, border_radius=GameUnit(15).pixels)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_SHIFT:
                self.is_opened = not self.is_opened
                print("toggled console")
                return True

        if not self.is_opened:
            return False

        if event.type != pygame.KEYDOWN:
            return False

        char = event.unicode
        print(f"console got {char}")
        if event.key == pygame.K_RETURN:
            command_text = self._input_text
            self._input_text = ""
            parsed_command = self._parse_command(command_text)
            if parsed_command:
                self._do_task(parsed_command)
            return True
        elif event.key == pygame.K_BACKSPACE:
            self._input_text = self._input_text[0:-2]
            return True
        elif char is not None and (char.isalnum() or char == " "):
            self._input_text += char
            return True
        return False
