"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class StartState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings


class StartState(BaseState):
    def enter(self) -> None:
        pygame.mixer.music.load(settings.MUSIC["start"])
        pygame.mixer.music.play(loops=-1)

    def exit(self) -> None:
        pygame.mixer.music.stop()

    def render(self, surface: pygame.Surface) -> None:
        background = settings.TEXTURES["background"]
        surface.blit(
            pygame.transform.scale(background, (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)),
            (0, 0),
        )

        render_text(
            surface,
            "The Legend of the Princess",
            settings.FONTS["princess"],
            settings.VIRTUAL_WIDTH / 2 + 2,
            settings.VIRTUAL_HEIGHT / 2 - 30,
            settings.COLOR_TITLE_SHADOW,
            center=True,
        )
        render_text(
            surface,
            "The Legend of the Princess",
            settings.FONTS["princess"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - 32,
            settings.COLOR_TITLE,
            center=True,
        )
        render_text(
            surface,
            "Press Enter",
            settings.FONTS["princess-small"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 + 64,
            settings.COLOR_WHITE,
            center=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("play")
