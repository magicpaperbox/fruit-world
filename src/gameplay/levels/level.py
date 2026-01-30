from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map import Map
from gameplay.levels.map.direction import Direction
from gameplay.levels.strawberry_quest import StrawberryQuest
from gameplay.player.inventory import Inventory
from render.debug import draw_area, draw_rect


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

    def draw_level(self, game_surface, player):
        self.current_map.background_img.draw(game_surface)
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
        for collectible_object in self.current_map.collectible_objects:
            collectible_object.draw(game_surface)

        player.draw(game_surface)

    def draw_debug(self, game_surface, move_player):
        draw_area(game_surface, self.current_map.strawberry_bushes, (190, 20, 40), "TRUS")
        draw_area(game_surface, self.current_map.blueberry_bushes, (60, 120, 255), "BOR")
        draw_rect(game_surface, move_player.collision_rect_x, (250, 250, 0), "HIT")
        draw_rect(game_surface, move_player.collision_rect_y, (250, 165, 20), "HIT")
        for platform in self.current_map.platforms:
            draw_rect(
                game_surface,
                platform.rect,
                (0, 230, 0),
                f"{platform.rect.left}x{platform.rect.top}",
            )

    def update_level(self, now_ms: int):
        for collectible in self.current_map.collectible_objects:
            collectible.update(now_ms)
