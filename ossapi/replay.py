from functools import cached_property

from osrparse import GameMode as OsrparseGameMode

from ossapi.models import GameMode, User, Beatmap
from ossapi.mod import Mod
from ossapi.enums import UserLookupKey

game_mode_map = {
    OsrparseGameMode.STD:   GameMode.STD,
    OsrparseGameMode.TAIKO: GameMode.TAIKO,
    OsrparseGameMode.CTB:   GameMode.CTB,
    OsrparseGameMode.MANIA: GameMode.MANIA,
}

class Replay:
    """
    A thin shim around an osrparse.Replay instance. Converts some attributes to
    more appropriate types and adds a few api related methods.
    """
    def __init__(self, replay, api):
        self._api = api
        self.game_mode = game_mode_map[replay.game_mode]
        self.game_version = replay.game_version
        self.beatmap_hash = replay.beatmap_hash
        self.player_name = replay.player_name
        self.replay_hash = replay.replay_hash
        self.count_300 = replay.number_300s
        self.count_100 = replay.number_100s
        self.count_50 = replay.number_50s
        self.count_geki = replay.gekis
        self.count_katu = replay.katus
        self.count_miss = replay.misses
        self.score = replay.score
        self.max_combo = replay.max_combo
        self.is_perfect_combo = replay.is_perfect_combo
        self.mods = Mod(replay.mod_combination.value)
        self.life_bar_graph = replay.life_bar_graph
        self.timestamp = replay.timestamp
        self.play_data = replay.play_data
        self.replay_id = replay.replay_id

    @cached_property
    def beatmap(self) -> Beatmap:
        return self._api.beatmap(checksum=self.beatmap_hash)

    @cached_property
    def user(self) -> User:
        return self._api.user(self.player_name, key=UserLookupKey.USERNAME)
