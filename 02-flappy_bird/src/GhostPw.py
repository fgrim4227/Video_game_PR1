import pygame
from src.Bird import Bird
from src.PowerUp import PowerUp
import settings
import math
class GhostPw(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
    def update(self, dt:float):
        self.timer += dt
        self.x += -settings.MAIN_SCROLL_SPEED * dt
        self.y = self.ogy + 15 * math.sin(self.timer * 5)
    def taken(self, bird : Bird):
        if not bird.is_ghost:
            pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "ghost.mp3")
            pygame.mixer.music.play(loops=-1)
            
        bird.is_ghost = True
        bird.power_up_timer += 5.0

    def render(self, surface: pygame.Surface):
        surface.blit(settings.TEXTURES["ghost"], self.get_rect())
