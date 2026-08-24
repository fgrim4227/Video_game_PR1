"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World
from src.Strategy import Strategy
from src.HardMode import HardMode
from src.EasyMode import EasyMode

class TitleScreenState(BaseState):
    def enter(self) -> None:
        #Por ahora, tenemos que actualizarlo
        self.dif : Strategy = Strategy()
        self.world = World(self.dif)
        self.option = 1
        pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "marios_way.ogg")
        pygame.mixer.music.play(loops=-1)

    def update(self, dt: float) -> None:
        self.world.update(dt, 0)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Press Enter to select",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        colorop1 = settings.COLOR_HIGHLIGHT if (self.option == 0) else settings.COLOR_WHITE
        render_text(
            surface,
            "Easy Mode",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 3,
            2 * settings.VIRTUAL_HEIGHT / 3,
            colorop1,
            center=True,
            shadowed=True,
        )
        colorop2 = settings.COLOR_HIGHLIGHT if (self.option == 1) else settings.COLOR_WHITE
        render_text(
            surface,
            "Hard Mode",
            settings.FONTS["medium"],
            2 * settings.VIRTUAL_WIDTH / 3,
            2 * settings.VIRTUAL_HEIGHT / 3,
            colorop2,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            self.dif = EasyMode() if self.option == 0 else HardMode()
            self.state_machine.change("count_down", self.dif)
        if(input_id == "left" and input_data.pressed):
            self.option = max(0, self.option - 1)
        if(input_id == "right" and input_data.pressed):
            self.option = min(1, self.option + 1)
