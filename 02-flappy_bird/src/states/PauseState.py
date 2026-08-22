import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World

class PauseState(BaseState):
    def enter(self, world : World, bird : Bird, score : int) -> None:
        self.world = world
        self.bird = bird
        self.paused = True
        self.score = score
    def update(self, dt: float) -> None:
        pass
    def render(self, surface : pygame.surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
                    surface,
                    f"||",
                    settings.FONTS["huge"],
                    settings.VIRTUAL_WIDTH / 2,
                    settings.VIRTUAL_HEIGHT / 2,
                    settings.COLOR_WHITE,
                    center = True,
                    shadowed=True,
                )
        render_text(
                    surface,
                    f"Score: {self.score}",
                    settings.FONTS["flappy"],
                    20,
                    10,
                    settings.COLOR_WHITE,
                    shadowed=True,
                )
    def on_input(self, input_id : str, input_data : InputData):
        if(input_id == "pause" and input_data.pressed) and self.paused:
            self.state_machine.change("playing", self.world, self.bird, self.score)

