"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class TitleState.
"""

import random

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.rendering import render_table

from src.Paddle import Paddle
from src.Bot import Bot

class TitleState(BaseState):
    def enter(self, pong) -> None:
        self.pong = pong
        self.selected_opt = 0

    def render(self, surface: pygame.Surface) -> None:
        render_table(surface, self.pong)
        render_text(
            surface,
            "Press enter to select",
            settings.FONTS["score"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - 32,
            settings.COLOR_WHITE,
            center=True,
        )

        color_t1 = (255,255,0) if (self.selected_opt == 0) else settings.COLOR_WHITE
        color_t2 = (255,255,0) if (self.selected_opt == 1) else settings.COLOR_WHITE
        color_t3 = (255,255,0) if (self.selected_opt == 2) else settings.COLOR_WHITE

        render_text(surface, "2 Jugadores", settings.FONTS["large"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 30, color_t1, center=True)
        render_text(surface, "1 Jugador vs Bot", settings.FONTS["large"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 50, color_t2, center=True)
        render_text(surface, "Bot vs Bot", settings.FONTS["large"], settings.VIRTUAL_WIDTH / 2, settings.VIRTUAL_HEIGHT / 2 + 70, color_t3, center=True)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if((input_id == "p1_down" or input_id == "p2_down") and input_data.pressed):
            self.selected_opt = (self.selected_opt + 1) % 3
        elif((input_id == "p1_up" or input_id == "p2_up") and input_data.pressed):
                self.selected_opt = ((self.selected_opt - 1) + 3) % 3
        elif(input_id == "confirm" and input_data.pressed):
            if(self.selected_opt == 0):
                  self.pong.player1 = Paddle(settings.PADDLE_X_OFFSET,
                              settings.PADDLE_Y_OFFSET,
                              settings.PADDLE_WIDTH,
                              settings.PADDLE_HEIGHT,)
                  self.pong.player2 = Paddle(
                        settings.VIRTUAL_WIDTH - settings.PADDLE_WIDTH - settings.PADDLE_X_OFFSET,
                        settings.VIRTUAL_HEIGHT - settings.PADDLE_HEIGHT - settings.PADDLE_Y_OFFSET,
                        settings.PADDLE_WIDTH,
                        settings.PADDLE_HEIGHT,
                    )
            elif(self.selected_opt == 1):
                self.pong.player1 = Paddle(settings.PADDLE_X_OFFSET,
                    settings.PADDLE_Y_OFFSET,
                    settings.PADDLE_WIDTH,
                    settings.PADDLE_HEIGHT,)
                self.pong.player2 = Bot( settings.VIRTUAL_WIDTH - settings.PADDLE_WIDTH - settings.PADDLE_X_OFFSET,
                    settings.VIRTUAL_HEIGHT - settings.PADDLE_HEIGHT - settings.PADDLE_Y_OFFSET,
                    settings.PADDLE_WIDTH,
                    settings.PADDLE_HEIGHT, self.pong.ball
                )
            elif(self.selected_opt == 2):
                self.pong.player1 = Bot(settings.PADDLE_X_OFFSET,
                    settings.PADDLE_Y_OFFSET,
                    settings.PADDLE_WIDTH,
                    settings.PADDLE_HEIGHT, self.pong.ball)
                self.pong.player2 = Bot( settings.VIRTUAL_WIDTH - settings.PADDLE_WIDTH - settings.PADDLE_X_OFFSET,
                    settings.VIRTUAL_HEIGHT - settings.PADDLE_HEIGHT - settings.PADDLE_Y_OFFSET,
                    settings.PADDLE_WIDTH,
                    settings.PADDLE_HEIGHT, self.pong.ball
                )
            self.state_machine.change("serve", pong=self.pong)