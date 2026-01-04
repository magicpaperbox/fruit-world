from gameplay.levels.level_spec import LevelSpec
from gameplay.levels.map import Map
from gameplay.levels.map.direction import Direction
from gameplay.levels.strawberry_quest import StrawberryQuest
from gameplay.player.inventory import Inventory


class Level:
    def __init__(self, inventory: Inventory, level_spec: LevelSpec):
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
