"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class DoneState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.rendering import render_table


class DoneState(BaseState):
    def enter(self, pong) -> None:
        self.pong = pong

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)
        render_text(
            surface,
            f"Player {self.pong.winning_player} won!",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
        )
        render_text(
            surface,
            "Press enter to restart",
            settings.FONTS["large"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            pong = self.pong
            pong.player1_score = 0
            pong.player2_score = 0
            pong.ball.reset(
                settings.VIRTUAL_WIDTH / 2 - settings.BALL_SIZE / 2,
                settings.VIRTUAL_HEIGHT / 2 - settings.BALL_SIZE / 2,
            )
            pong.serving_player = 2 if pong.winning_player == 1 else 1
            self.state_machine.change("serve", pong=pong)
        elif(input_id == "menu" and input_data.pressed):
                    pong = self.pong
                    pong.reset()
                    self.state_machine.change("title", pong=pong)
        
