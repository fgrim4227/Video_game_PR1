import pygame
from src.Bird import Bird
import settings
class PowerUp:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.ogy = y
        self.timer = 0.0
        self.width =  settings.POWER_UP_SIZE 
        self.height = settings.POWER_UP_SIZE

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def taken(self, bird: Bird):
        pass

    def update(self, dt: float):
        pass

    def render(self, surface: pygame.Surface):
        pass