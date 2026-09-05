"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameObject.
"""

from typing import Any, Dict

import pygame

import settings


class GameObject:
    def __init__(self, definition: Dict[str, Any], x: float, y: float) -> None:
        self.type = definition["type"]
        self.texture_id = definition["texture"]
        self.frame_index = definition.get("frame", 1)

        # Whether it acts as an obstacle or not.
        self.solid = definition["solid"]

        self.default_state = definition["default_state"]
        self.state = self.default_state
        self.states = definition["states"]

        self.x = x
        self.y = y
        self.width = definition["width"]
        self.height = definition["height"]

        self.on_collide = definition.get("on_collide") or (lambda: None)

        # Whether this object is consumable or not.
        self.consumable = definition.get("consumable", False)
        self.on_consume = definition.get("on_consume") or (lambda player, obj: None)

        #Interactables
        self.interactable = definition.get("interactable", False)
        self.on_interact = definition.get("on_interact") or (lambda player, obj: None)
        # An object could be taken or not.
        self.takeable = definition.get("takeable", False)
        self.taken = False

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        frame_index = self.states[self.state].get("frame", self.frame_index)
        surface.blit(
            settings.TEXTURES[self.texture_id],
            (self.x + offset_x, self.y + offset_y),
            settings.frame(self.texture_id, frame_index),
        )
