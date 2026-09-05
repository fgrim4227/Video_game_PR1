"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the base class BaseEntityState.
"""

from typing import TypeVar

from gale.state import BaseState, StateMachine


class BaseEntityState(BaseState):
    def __init__(
        self, entity: TypeVar("Entity"), state_machine: StateMachine
    ) -> None:
        super().__init__(state_machine)
        self.entity = entity

    def process_ai(self, room: TypeVar("Room"), dt: float) -> None:
        """
        AI decision-making for entities driven by Room's update loop, kept
        separate from update() (which just applies movement/collision) so
        player states — which have no AI — can reuse the movement half
        without dragging AI logic along. No-op by default.
        """
        pass
