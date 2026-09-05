"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Doorway.
"""

from typing import Any, TypeVar

import pygame

import settings


class Doorway:
    def __init__(self, direction: str, open_: bool, room: TypeVar("Room")) -> None:
        self.direction = direction
        self.open = open_
        self.room = room

        if direction == "left":
            self.x = settings.MAP_RENDER_OFFSET_X
            self.y = (
                settings.MAP_RENDER_OFFSET_Y
                + settings.MAP_HEIGHT // 2 * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.height = 32
            self.width = 16
        elif direction == "right":
            self.x = (
                settings.MAP_RENDER_OFFSET_X
                + settings.MAP_WIDTH * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.y = (
                settings.MAP_RENDER_OFFSET_Y
                + settings.MAP_HEIGHT // 2 * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.height = 32
            self.width = 16
        elif direction == "top":
            self.x = (
                settings.MAP_RENDER_OFFSET_X
                + settings.MAP_WIDTH // 2 * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.y = settings.MAP_RENDER_OFFSET_Y
            self.height = 16
            self.width = 32
        else:
            self.x = (
                settings.MAP_RENDER_OFFSET_X
                + settings.MAP_WIDTH // 2 * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.y = (
                settings.MAP_RENDER_OFFSET_Y
                + settings.MAP_HEIGHT * settings.TILE_SIZE
                - settings.TILE_SIZE
            )
            self.height = 16
            self.width = 32

    def render(
        self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0
    ) -> None:
        texture = settings.TEXTURES["tiles"]

        # Used for shifting the doors when sliding rooms.
        x = self.x + offset_x
        y = self.y + offset_y

        def draw(frame_number: int, dx: float, dy: float) -> None:
            surface.blit(texture, (x + dx, y + dy), settings.frame("tiles", frame_number))

        if self.direction == "left":
            if self.open:
                draw(181, -settings.TILE_SIZE, 0)
                draw(182, 0, 0)
                draw(200, -settings.TILE_SIZE, settings.TILE_SIZE)
                draw(201, 0, settings.TILE_SIZE)
            else:
                draw(219, -settings.TILE_SIZE, 0)
                draw(220, 0, 0)
                draw(238, -settings.TILE_SIZE, settings.TILE_SIZE)
                draw(239, 0, settings.TILE_SIZE)
        elif self.direction == "right":
            if self.open:
                draw(172, 0, 0)
                draw(173, settings.TILE_SIZE, 0)
                draw(191, 0, settings.TILE_SIZE)
                draw(192, settings.TILE_SIZE, settings.TILE_SIZE)
            else:
                draw(174, 0, 0)
                draw(175, settings.TILE_SIZE, 0)
                draw(193, 0, settings.TILE_SIZE)
                draw(194, settings.TILE_SIZE, settings.TILE_SIZE)
        elif self.direction == "top":
            if self.open:
                draw(98, 0, -settings.TILE_SIZE)
                draw(99, settings.TILE_SIZE, -settings.TILE_SIZE)
                draw(117, 0, 0)
                draw(118, settings.TILE_SIZE, 0)
            else:
                draw(134, 0, -settings.TILE_SIZE)
                draw(135, settings.TILE_SIZE, -settings.TILE_SIZE)
                draw(153, 0, 0)
                draw(154, settings.TILE_SIZE, 0)
        else:
            if self.open:
                draw(141, 0, 0)
                draw(142, settings.TILE_SIZE, 0)
                draw(160, 0, settings.TILE_SIZE)
                draw(161, settings.TILE_SIZE, settings.TILE_SIZE)
            else:
                draw(216, 0, 0)
                draw(217, settings.TILE_SIZE, 0)
                draw(235, 0, settings.TILE_SIZE)
                draw(236, settings.TILE_SIZE, settings.TILE_SIZE)

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)
