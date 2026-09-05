"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains move_and_bump: the room-boundary collision every walking
entity (AI-controlled or player-controlled) uses, shared so it is defined
in exactly one place instead of once per walk state.
"""

from typing import Any

import settings


def move_and_bump(entity: Any, dt: float) -> bool:
    """
    Moves entity by entity.walk_speed * dt along entity.direction, clamping
    it to the room's walkable area.

    :returns: Whether the entity was stopped short by the room's boundary.
    """
    bumped = False

    if entity.direction == "left":
        entity.x -= entity.walk_speed * dt
        limit = settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE

        if entity.x <= limit:
            entity.x = limit
            bumped = True
    elif entity.direction == "right":
        entity.x += entity.walk_speed * dt
        limit = settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2

        if entity.x + entity.width >= limit:
            entity.x = limit - entity.width
            bumped = True
    elif entity.direction == "up":
        entity.y -= entity.walk_speed * dt
        limit = settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE - entity.height / 2

        if entity.y <= limit:
            entity.y = limit
            bumped = True
    elif entity.direction == "down":
        entity.y += entity.walk_speed * dt
        bottom_edge = (
            settings.MAP_HEIGHT * settings.TILE_SIZE
            + settings.MAP_RENDER_OFFSET_Y
            - settings.TILE_SIZE
        )

        if entity.y + entity.height >= bottom_edge:
            entity.y = bottom_edge - entity.height
            bumped = True

    return bumped
