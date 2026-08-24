import pygame
from typing import Optional
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.Strategy import Strategy

class GameOverState(BaseState):
    def enter(self, world: World, bird: Bird, difficulty: Strategy) -> None:
        self.world = world
        self.bird = bird
        self.bird.vx = 0
        self.difficulty = difficulty
        self.option = 0
        settings.SOUNDS["game_over"].play()

    def update(self, dt: float) -> None:
        self.bird.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        
        render_text(
            surface, 
            "Game Over", 
            settings.FONTS["huge"], 
            settings.VIRTUAL_WIDTH / 2, 
            settings.VIRTUAL_HEIGHT / 4, 
            (255, 0, 0), 
            center=True, 
            shadowed=True
        )
        colorop1 = settings.COLOR_HIGHLIGHT if self.option == 0 else settings.COLOR_WHITE
        render_text(
            surface,
            "Restart",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 3,
            2 * settings.VIRTUAL_HEIGHT / 3,
            colorop1,
            center=True,
            shadowed=True,
        )
        
        colorop2 = settings.COLOR_HIGHLIGHT if self.option == 1 else settings.COLOR_WHITE
        render_text(
            surface,
            "Main Menu",
            settings.FONTS["medium"],
            2 * settings.VIRTUAL_WIDTH / 3,
            2 * settings.VIRTUAL_HEIGHT / 3,
            colorop2,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "left" and input_data.pressed:
            self.option = max(0, self.option - 1)
        if input_id == "right" and input_data.pressed:
            self.option = min(1, self.option + 1)
        if input_id == "confirm" and input_data.pressed:
            if self.option == 0:
                pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "marios_way.ogg")
                pygame.mixer.music.play(loops=-1)
                self.state_machine.change("count_down", self.difficulty)
            else:
                self.state_machine.change("title")