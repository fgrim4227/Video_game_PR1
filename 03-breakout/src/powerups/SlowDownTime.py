from typing import TypeVar
from src.powerups.PowerUp import PowerUp
from src.strategys.SSlowDownTime import StratSlowTime

class SlowDownTime(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)
        self.frame = 4

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.add_strategy("slow_time", StratSlowTime(), 7)
        self.active = False