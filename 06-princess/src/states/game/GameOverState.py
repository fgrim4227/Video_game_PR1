"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameOverState for the game.
"""

from typing import TypeVar

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings


class GameOverState(BaseState):
    def enter(self, player: TypeVar("Player")) -> None:
        self.player = player
        pygame.mixer.music.load(settings.MUSIC["game-over"])
        pygame.mixer.music.play()

    def exit(self) -> None:
        pygame.mixer.music.stop()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            self.state_machine.change("start")

    def render(self, surface: pygame.Surface) -> None:
        render_text(
            surface,
            "GAME OVER",
            settings.FONTS["princess"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - 48,
            settings.COLOR_TITLE,
            center=True,
        )
        render_text(
            surface,
            "Press Enter",
            settings.FONTS["princess-small"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 + 16,
            settings.COLOR_WHITE,
            center=True,
        )
