"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Ball.
"""

import pygame

import settings


class Ball:
    def __init__(self, x: float, y: float, size: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = size
        self.height: float = size
        self.vx: float = 0.0
        self.vy: float = 0.0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        self.x += self.vx * dt
        self.y += self.vy * dt

    def reset(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, settings.COLOR_YELLOW, self.get_rect())
