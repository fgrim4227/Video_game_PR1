"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

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
            10, 
            [(self, {"fade_alpha": 255})], 
            on_finish=lambda: self.state_machine.change("play", level = self.level + 1) 
        )


    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
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
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)

    def _spawn_key(self, x, y):
            from src.GameItem import GameItem
            from gale.timer import Timer
            #Temporal
            key = GameItem(
                x, y, 16, 16, "tiles", 61, 
                collidable=True, consumable=True, 
                on_consume=self._win_level
            )
            Timer.tween(
                1.5, 
                [(key, {"y": y - 10})], 
                ease_function_name= "linear"
            )
            self.game_level.items.append(key)

    def _win_level(self, item, player):
        from gale.timer import Timer
        settings.SOUNDS["victory"].play()
        self.clock.pause_and_unpause()

        for game_item in self.game_level.items:
            game_item.collidable = False

        self.fade_alpha = 0
        Timer.tween(
            1.5, 
            [(self, {"fade_alpha": 255})], 
            on_finish=lambda: self.state_machine.change("start") 
        )
