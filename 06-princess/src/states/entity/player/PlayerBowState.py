from typing import TypeVar
from gale.state import StateMachine
from src.states.entity.BaseEntityState import BaseEntityState
from src.ArrowFactory import ArrowFactory

class PlayerBowState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.timer = 0

    def enter(self) -> None:
        self.entity.change_animation(f"bow-{self.entity.direction}")
        arrow = ArrowFactory.create(self.entity)
        self.dungeon.current_room.projectiles.append(arrow)
        self.timer = 0.2

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
    def update(self, dt: float) -> None:
        self.timer -= dt
        if self.timer <= 0:
            self.entity.change_state("idle")