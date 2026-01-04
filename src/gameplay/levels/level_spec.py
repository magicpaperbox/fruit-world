from gameplay.levels.map.map_spec import MapSpec


class LevelSpec:
    def __init__(self, maps: list[MapSpec], initial_map_id: str):
        self.maps = maps
        self.initial_map_id = initial_map_id
