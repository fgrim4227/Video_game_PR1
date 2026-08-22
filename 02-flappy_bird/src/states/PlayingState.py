"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.HardMode import HardMode
from src.EasyMode import EasyMode
from src.Strategy import Strategy
class PlayingState(BaseState):
    def enter(self, world: Optional[World] = None, bird : Optional[Bird] = None, score : int = 0, difficulty : Optional[Strategy] = None) -> None:
        self.difficulty = difficulty if difficulty is not None else HardMode()
        self.world = world if world is not None else World(difficulty)
        self.world.reset(True)
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.score = score

    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt, self.score)

        if self.world.collides(self.bird.get_rect()):
            settings.SOUNDS["explosion"].play()
            settings.SOUNDS["hurt"].play()
            self.state_machine.change("count_down", self.difficulty)
            return

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()
        if(input_id == "pause" and input_data.pressed):
            self.state_machine.change("pause", self.world, self.bird, self.score)
        print("Even regitsts?")
        print(input_id)
        self.difficulty.handle_input(input_id, input_data, self.bird)
