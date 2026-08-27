from typing import TypeVar
from src.powerups.PowerUp import PowerUp
from src.strategys.SGrabBalls import StratGrabBalls

class GrabBalls(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)
        self.frame = 2
        
    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.add_strategy("grab_balls", StratGrabBalls(), 7) 
        self.active = False