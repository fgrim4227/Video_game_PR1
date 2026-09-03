
from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player


class VictoryState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        pygame.mixer.music.stop()
        settings.SOUNDS["victory"].play()
        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")

        self.camera = enter_params.get("camera")

        self.clock = enter_params.get("clock")

        self.clock.pause_and_unpause()
        for game_item in self.game_level.items:
                    game_item.collidable = False
        
        self.fade_alpha = 0
        Timer.tween(
            6.8, 
            [(self, {"fade_alpha": 255})], 
            on_finish= self._go_to_next
        )

    def _go_to_next(self):
        if self.level < settings.NUM_LEVELS:
            pygame.mixer.music.load(
                                        settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
                                    )
            pygame.mixer.music.play(loops=-1)
            self.state_machine.change("play", level=self.level + 1)
        else:
            self.state_machine.change("game_completed_state", player=self.player)
    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        for block in self.game_level.special_blocks:
            if block["hit"]:
                empty_block_img = settings.FRAMES["tiles"][69] 

                rect = self.camera.apply(pygame.Rect(block["x"], block["y"], block["width"], block["height"]))
                
                surface.blit(settings.TEXTURES["tiles"], (rect.x, rect.y), empty_block_img)
        self.player.render(surface, self.camera)

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
            shadowed=True,
        )
        if hasattr(self, 'fade_alpha') and self.fade_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.fade_alpha))
            surface.blit(fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        pass
