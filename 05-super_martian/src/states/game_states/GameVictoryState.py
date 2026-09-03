import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings

class GameCompletedState(BaseState):
    def enter(self, player) -> None:
        self.player = player
        pygame.mixer.music.stop()

        settings.SOUNDS["victory"].play()

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((25, 130, 196))

        render_text(
            surface,
            "CONGRATULATIONS!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            40,
            (255, 215, 0),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "You beat the game!",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            70,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            f"Final Score: {self.player.score}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            110,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "Press Enter to return to Title",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 30,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            settings.SOUNDS["victory"].stop()
            self.state_machine.change("start")