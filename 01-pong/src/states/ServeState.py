"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class ServeState.
"""

import random

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.rendering import render_table


class ServeState(BaseState):
    def enter(self, pong) -> None:
        self.pong = pong

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)
        render_text(
            surface,
            "Press enter to serve",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            pong = self.pong
            pong.ball.vx = random.randint(140, 199)

            if pong.serving_player == 2:
                pong.ball.vx *= -1

            pong.ball.vy = random.randint(-50, 49)
            self.state_machine.change("play", pong=pong)
        elif(input_id == "menu" and input_data.pressed):
            pong = self.pong
            pong.reset()
            self.state_machine.change("title", pong=pong)
