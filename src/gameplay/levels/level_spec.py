from gameplay.levels.map_spec import MapSpec


class LevelSpec:
    def __init__(self, maps: list[MapSpec], initial_map_id: str, music_path: str):
        self.maps = maps
        self.initial_map_id = initial_map_id
        self.music_path = music_path
