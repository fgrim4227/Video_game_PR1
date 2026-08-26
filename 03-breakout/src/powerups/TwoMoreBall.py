from typing import TypeVar
from src.powerups.PowerUp import PowerUp
from src.strategys.SMoreBalls import StratMoreBalls

class TwoMoreBall(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.add_strategy("more_balls", StratMoreBalls(), 0)
        self.active = False