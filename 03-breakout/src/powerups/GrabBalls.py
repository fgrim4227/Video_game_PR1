import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp


class GrabBalls(PowerUp):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)
        self.frame = 2
    t = TypeVar("PlayState")
    def take(self, play_state: t) -> None:
        paddle = play_state.paddle
        paddle.activate_grab()
        self.active = False