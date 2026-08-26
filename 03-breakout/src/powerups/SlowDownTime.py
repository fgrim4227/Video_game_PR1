import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class SlowDownTime(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)
        self.frame = 4

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.can_slow = True
        paddle.slow_window = 7
        self.active = False
