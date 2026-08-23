"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair
from src.Strategy import Strategy
from src.EasyMode import EasyMode
from src.HardMode import HardMode
from src.PowerUp import PowerUp
class World:
    def __init__(self, dificulty : Strategy, generate_logs: bool = False) -> None:
        self.generate_logs: bool = generate_logs
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        self.current_limit = settings.TIME_TO_SPAWN_LOGS
        self.logs: List[LogPair] = []
        self.logs_spawn_timer: float = 0.0
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.dif : Strategy = dificulty
        self.pw_up = []

    def reset(self, generate_logs: bool) -> None:
        self.generate_logs = generate_logs

    def collides(self, rect: pygame.Rect) -> bool:
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)
    def pw_collition(self, rect: pygame.Rect) -> PowerUp:
        for pw in self.pw_up:
            if pw.collides(rect):
                return pw
        return None
    def update(self, dt: float, score) -> None:
        self.dif.generation(self, dt, score)
        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0
        for pw in self.pw_up:
            pw.update(dt)
        self.pw_up = [pw for pw in self.pw_up if pw.x > -50]

        for log_pair in self.logs:
            log_pair.update(dt)

        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
        for pw in self.pw_up:
            pw.render(surface)
