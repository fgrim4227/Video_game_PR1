
from gale.timer import Timer
from src.states.entities.BaseEntityState import BaseEntityState

class SnailDeadState(BaseEntityState):
    def enter(self, *args, **kwargs) -> None:
        self.entity.change_animation("dead")
        self.entity.vx = 0

        Timer.after(0.5, lambda: setattr(self.entity, 'is_dead', True))

    def update(self, dt: float) -> None:
        pass