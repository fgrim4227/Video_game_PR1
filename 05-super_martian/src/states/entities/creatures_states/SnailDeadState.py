from gale.timer import Timer
from src.states.entities.BaseEntityState import BaseEntityState

class SnailDeadState(BaseEntityState):
    def enter(self, *args, **kwargs) -> None:
        self.entity.change_animation("dead")
        self.entity.vx = 0
        self.flipped = kwargs.get("flipped", False)
        Timer.after(5, self._revive)

    def _revive(self):
        if not getattr(self.entity, 'is_dead', False):
            self.entity.change_state("walk", self.flipped)
            self.entity.is_dying = False

    def update(self, dt: float) -> None:
        pass