"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class JumpState for player.
"""

import settings
from src.states.entities.BaseEntityState import BaseEntityState


class JumpState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation("jump")
        self.entity.vy = -settings.JUMP_TAKEOFF_SPEED
        settings.SOUNDS["jump"].play()

    def update(self, dt: float) -> None:
        self.entity.jump_requested = False

        # Releasing "jump" while still ascending clamps the upward speed
        # down to JUMP_CUT_VELOCITY instead of zeroing it outright, so a
        # tap still gives a small hop rather than an abrupt stop.
        if not self.entity.jump_held and self.entity.vy < -settings.JUMP_CUT_VELOCITY:
            self.entity.vy = -settings.JUMP_CUT_VELOCITY

        if self.entity.move_direction != 0:
            self.entity.flipped = self.entity.move_direction < 0
        self.entity.vx = settings.PLAYER_SPEED * self.entity.move_direction

        if self.entity.vy >= 0:
            self.entity.change_state("fall")
