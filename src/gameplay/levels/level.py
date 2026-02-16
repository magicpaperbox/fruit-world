import pygame

import screen.scale_screen as ss
from gameplay.levels.direction import Direction
from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map import Map
from gameplay.levels.strawberry_quest import StrawberryQuest
from gameplay.player.inventory import Inventory
from gameplay.player.player import Player
from render.debug import DEBUG_RENDERER
from render.debuggable import Debuggable


class Level:
    def __init__(self, inventory: Inventory, level_spec: LevelSpec):
        self.music_path = level_spec.music_path
        self._maps = {}
        for map_spec in level_spec.maps:
            map = Map(map_spec)
            self._maps[map_spec.map_id] = map

        self.current_map = self._maps[level_spec.initial_map_id]

        mouse = self.current_map.npcs[0]
        strawberry_quest = StrawberryQuest(mouse, inventory)
        strawberry_quest.start()
        self.quests = [strawberry_quest]

    def try_load_map(self, direction: Direction) -> bool:
        next_map_id = self.current_map.neighbours.get(direction)
        if not next_map_id:
            return False
        self.current_map = self._maps[next_map_id]
        return True

    def draw_level(self, game_surface: pygame.Surface):
        self.current_map.background_img.draw(game_surface)
        for hazardous_obj in self.current_map.hazard:
            hazardous_obj.draw(game_surface)
        for platform in self.current_map.platforms:
            platform.draw(game_surface)
        for bush in self.current_map.blueberry_bushes:
            bush.draw(game_surface)
        for bush in self.current_map.strawberry_bushes:
            bush.draw(game_surface)
        for obj in self.current_map.static_objects:
            obj.draw(game_surface)
        for npc in self.current_map.npcs:
            npc.draw(game_surface)
        for consumable_object in self.current_map.consumable_objects:
            consumable_object.draw(game_surface)

    def draw_debug(self, game_surface, debuggables: list[Debuggable]):
        DEBUG_RENDERER.draw_area(game_surface, self.current_map.strawberry_bushes, (190, 20, 40), "TRUS")
        DEBUG_RENDERER.draw_area(game_surface, self.current_map.blueberry_bushes, (60, 120, 255), "BOR")
        for d in debuggables:
            d.draw_debug(game_surface)
        for hazardous_obj in self.current_map.hazard:
            DEBUG_RENDERER.draw_rect(
                game_surface,
                hazardous_obj.rect,
                (0, 150, 120),
                f"{hazardous_obj.rect.left}x{hazardous_obj.rect.top}",
            )

        for platform in self.current_map.platforms:
            DEBUG_RENDERER.draw_rect(
                game_surface,
                platform.rect,
                (0, 230, 0),
                f"{platform.rect.left}x{platform.rect.top}",
            )

    def change_map(self, player: Player):
        if player.player_rect.centerx > ss.GAME_WIDTH:
            if self.try_load_map(Direction.RIGHT):
                player.set_x_position(0)
            else:
                reset_player = ss.GAME_WIDTH - player.player_rect.width
                player.set_x_position(reset_player)
        elif player.player_rect.centerx <= 0:
            if self.try_load_map(Direction.LEFT):
                reset_player = ss.GAME_WIDTH - player.player_rect.width
                player.set_x_position(reset_player)
            else:
                player.set_x_position(0)

    def update_level(self, now_ms: int):
        for consumable in self.current_map.consumable_objects:
            consumable.update(now_ms)
