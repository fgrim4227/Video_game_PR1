"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Paddle.
"""

import pygame

import settings


class Paddle:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        self.y = max(0, min(self.y, settings.VIRTUAL_HEIGHT - self.height))

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, settings.COLOR_WHITE, self.get_rect())

    def reset_prediction(self)->None:
        pass
