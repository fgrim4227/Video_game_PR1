import pygame
import math
import settings

class TargetProjectile:
    def __init__(self, x: float, y: float, target_x: float, target_y: float, speed=70) -> None:
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
        self.dead = False
        dx = target_x - self.x
        dy = target_y - self.y
        magnitude = math.sqrt(dx**2 + dy**2)
        
        if magnitude != 0:
            self.vx = (dx / magnitude) * speed
            self.vy = (dy / magnitude) * speed
        else:
            self.vx, self.vy = 0, 0

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)
    
    def collides(self, target) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())
    def update(self, dt: float) -> None:
        if self.dead:
            return
            
        self.x += self.vx * dt
        self.y += self.vy * dt

        if (self.x < settings.MAP_RENDER_OFFSET_X or 
            self.x > settings.VIRTUAL_WIDTH or 
            self.y < settings.MAP_RENDER_OFFSET_Y or 
            self.y > settings.VIRTUAL_HEIGHT):
            self.dead = True

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        pygame.draw.circle(surface, (255, 69, 0), (int(self.x + offset_x), int(self.y + offset_y)), 4)