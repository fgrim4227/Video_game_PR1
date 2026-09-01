"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for creatures.
"""

from typing import Any, Dict, List

from src.states.entities import creatures_states

SPECIAL_BLOCKS: Dict[int, Dict[str, Any]] = {
    0: {
        "texture_id": "special_blocks",
        "hit": False,
    }
}