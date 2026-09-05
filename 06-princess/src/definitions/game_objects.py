"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for game objects.
"""

from typing import Any, Dict

import settings


def _pickup_heart(player, obj) -> None:
    player.heal(2)
    settings.SOUNDS["heart-taken"].play()

def _open_chest(player, obj) -> None:
    if obj.state == "closed":
        obj.state = "open"
        player.has_bow = True
        settings.SOUNDS["door"].play()
GAME_OBJECT_DEFS: Dict[str, Dict[str, Any]] = {
    "switch": {
        "type": "switch",
        "texture": "switches",
        "frame": 2,
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "unpressed",
        "states": {
            "unpressed": {"frame": 2},
            "pressed": {"frame": 1},
        },
    },
    "pot": {
        "type": "pot",
        "texture": "tiles",
        "frame": 16,
        "width": 16,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "default",
        "takeable": True,
        "states": {
            "default": {"frame": 16},
        },
    },
    # Definition of heart as a consumable object type.
    "heart": {
        "type": "heart",
        "texture": "hearts",
        "frame": 5,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": True,
        "default_state": "default",
        "states": {
            "default": {"frame": 5},
        },
        "on_consume": _pickup_heart,
    },
    #Chest
    "chest": {
        "type": "chest",
        "texture": "chests",
        "frame": 20,
        "width": 16,
        "height": 16,
        "solid": True,
        "interactable": True,
        "default_state": "closed",
        "states": {
            "closed": {"frame": 20},
            "open": {"frame": 21}, 
        },
        "on_interact": _open_chest,
    },
    #arrow
    "arrow": {
        "type": "arrow",
        "texture": "arrow",
        "frame": 1,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": False,
        "takeable": False,
        "default_state": "default",
        "states": {
            "default": {"frame": 1},
        },
    }
}
