"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameItem.
"""

from typing import Callable, TypeVar, Any, Optional

from src import mixins


class GameItem(mixins.DrawableMixin, mixins.CollidableMixin):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        texture_id: str,
        frame_index: int,
        collidable: bool,
        consumable: bool,
        on_collide: Optional[Callable[[TypeVar("GameItem"), Any], Any]] = None,
        on_consume: Optional[Callable[[TypeVar("GameItem"), Any], Any]] = None,
    ) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture_id = texture_id
        self.frame_index = frame_index
        self.flipped = False
        self.collidable = collidable
        self.consumable = consumable
        self._on_collide = on_collide
        self._on_consume = on_consume
        self.active = True

    def respawn(self, x: Optional[float] = None, y: Optional[float] = None) -> None:
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.active = True

    def on_collide(self, another: Any) -> Any:
        if not self.collidable or self._on_collide is None:
            return None
        return self._on_collide(self, another)

    def on_consume(self, consumer: Any) -> Any:
        if not self.consumable or self._on_consume is None:
            return None
        self.active = False
        return self._on_consume(self, consumer)
