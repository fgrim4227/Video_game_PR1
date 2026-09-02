import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.GameLevel import GameLevel

class DeadScreenState(BaseState):
    def enter(self, **enter_params) -> None:
        self.player = enter_params["player"]
        self.level = enter_params.get("level", 1)

        self.player.change_lives(-1)

        pygame.mixer.music.stop()


        print(self.player.lives)
        Timer.after(2.5, self._transition)

    def _transition(self):
        if self.player.lives > 0:
            new_game_level = GameLevel(self.level)
            self.state_machine.change("play", level=self.level, game_level=new_game_level, player=None, lives = self.player.lives)
        else:
           self.state_machine.change("game_over_transition", player=self.player)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        surface.blit(
            settings.TEXTURES["martian"],
            (settings.VIRTUAL_WIDTH // 2 - 30, settings.VIRTUAL_HEIGHT // 2 - 10),
            settings.FRAMES["martian"][4] 
        )

        render_text(
            surface,
            f"x {self.player.lives}",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2 + 10,
            settings.VIRTUAL_HEIGHT // 2,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        pass