"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class EntityIdleState.
"""

import random
from typing import TypeVar

import pygame

from src.states.entity.BaseEntityState import BaseEntityState


class EntityIdleState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation(f"idle-{self.entity.direction}")

        # Used for AI waiting.
        self.wait_duration = 0
        self.wait_timer = 0

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        if self.wait_duration == 0:
            self.wait_duration = random.randint(1, 5)
        else:
            self.wait_timer += dt

            if self.wait_timer > self.wait_duration:
                self.entity.change_state("walk")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
