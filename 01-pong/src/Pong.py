"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Pong as a specialization of gale.Game
"""

import pygame

from gale.game import Game
from gale.input_handler import InputData
from gale.state import StateMachine

import settings
from src import states
from src.Ball import Ball
from src.Paddle import Paddle
from src.Bot import Bot

class Pong(Game):
    def init(self) -> None:
        self.player1 = Paddle(
            settings.PADDLE_X_OFFSET,
            settings.PADDLE_Y_OFFSET,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
        self.player2 = Paddle(
            settings.VIRTUAL_WIDTH - settings.PADDLE_WIDTH - settings.PADDLE_X_OFFSET,
            settings.VIRTUAL_HEIGHT - settings.PADDLE_HEIGHT - settings.PADDLE_Y_OFFSET,
            settings.PADDLE_WIDTH,
            settings.PADDLE_HEIGHT,
        )
        self.ball = Ball(
            settings.VIRTUAL_WIDTH / 2 - settings.BALL_SIZE / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BALL_SIZE / 2,
            settings.BALL_SIZE,
        )
        self.player1_score = 0
        self.player2_score = 0
        self.serving_player = 1
        self.winning_player = 0

        self.state_machine = StateMachine(
            {
                "title": states.TitleState,
                "serve": states.ServeState,
                "play": states.PlayState,
                "done": states.DoneState,
            }
        )
        self.state_machine.change("title", pong=self)

    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "quit" and input_data.pressed:
            self.quit()
        else:
            self.state_machine.on_input(input_id, input_data)
    def reset(self)->None:
        self.ball.reset(settings.VIRTUAL_WIDTH / 2 - settings.BALL_SIZE / 2, 
                settings.VIRTUAL_HEIGHT / 2 - settings.BALL_SIZE / 2)
        self.player1_score = 0
        self.player2_score = 0
