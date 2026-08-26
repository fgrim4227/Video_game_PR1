import pygame
import settings

from typing import Any
class Missile():
    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 44
        self.vy = -settings.POWERUP_SPEED * 2
        self.active = True
        self.texture = settings.TEXTURES["missile"]
    def update(self, dt: float):
        self.y += self.vy * dt
        if(self.y <= 0):
            self.active = False

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, another : Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def render(self, surface : pygame.Surface):
        surface.blit(self.texture, (self.x, self.y))
    