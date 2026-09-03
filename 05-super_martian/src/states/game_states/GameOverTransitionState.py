import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings

class GameOverTransitionState(BaseState):
    def enter(self, **enter_params) -> None:
        self.player = enter_params["player"]
        self.fade_alpha = 0
        self.can_continue = False
        
        Timer.tween(
            3.5, 
            [(self, {"fade_alpha": 255})], 
            ease_function_name="linear",
            on_finish=lambda: setattr(self, 'can_continue', True)
        )

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        content_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        content_surface.fill((0, 0, 0))
        snail_img = settings.TEXTURES["evil_snail"]
        img_x = settings.VIRTUAL_WIDTH // 2 - snail_img.get_width() // 2
        img_y = settings.VIRTUAL_HEIGHT // 2 - snail_img.get_height() // 2 + 10
        content_surface.blit(snail_img, (img_x, img_y))
        render_text(
            content_surface,
            "GAME OVER",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            30,
            (255, 0, 0),
            center=True,
            shadowed=True,
        )
        content_surface.set_alpha(int(self.fade_alpha))
        surface.blit(content_surface, (0, 0))
        if self.can_continue:
            render_text(
                surface,
                "Press Enter to continue",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT - 20,
                (255, 255, 255),
                center=True,
                shadowed=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed and self.can_continue:
            self.state_machine.change("game_over", player=self.player)