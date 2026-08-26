"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Paddle.
"""

import pygame

import settings


class Paddle:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 64
        self.height = 16

        # By default, the blue paddle
        self.skin = 0

        # By default, the 64-pixels-width paddle.
        self.size = 1

        self.texture = settings.TEXTURES["spritesheet"]
        self.frames = settings.FRAMES["paddles"]

        # The paddle only move horizontally
        self.vx = 0

        self.grab = False
        self.missile = False
        self.can_slow = False
        self.slowing = False
        self.grab_time = 0
        self.missil_time = 0
        self.slow_window = 0
        self.slow_time = 0


    def resize(self, size: int) -> None:
        self.size = size
        self.width = (self.size + 1) * 32

    def dec_size(self):
        self.resize(max(0, self.size - 1))

    def inc_size(self):
        self.resize(min(3, self.size + 1))

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        next_x = self.x + self.vx * dt

        if self.vx < 0:
            self.x = max(0, next_x)
        else:
            self.x = min(settings.VIRTUAL_WIDTH - self.width, next_x)
        #Pudieramos hacer metodo que recorra booleanos
        if((self.grab) and self.grab_time >= 0):
            self.grab_time -= dt
        else:
            self.grab_time = 0
            self.grab = False
        if(self.missile and self.missil_time >= 0):
            self.missil_time -= dt
        else:
            self.missil_time = 0
            self.missile = False
            
        if(self.slow_window > 0 and self.can_slow):
            self.slow_window -= dt
        else:
            self.slow_window = 0
            self.can_slow = False
            
        if(self.slowing and self.slow_time >= 0):
            self.slow_time -= dt
        else:
            self.slow_time = 0
            self.slowing = False
    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y), self.frames[self.skin][self.size])
    def activate_grab(self):
        self.grab = True
        self.grab_time = 4
    def activate_missil(self):
        self.missile = True
        self.missil_time = 15
