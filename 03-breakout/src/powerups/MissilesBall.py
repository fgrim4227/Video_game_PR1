from typing import TypeVar
from src.powerups.PowerUp import PowerUp
from src.strategys.SMissil import StratMissil

class MissilesBall(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)
        self.frame = 3
        
    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.add_strategy("missil", StratMissil(), 8)
        self.active = False