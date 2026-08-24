"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame

import settings

import math
class Bird:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.jumping: bool = False
        self.is_ghost: bool = False
        self.power_up_timer = 0.0
        self.img_indx = 0
        self.frame_timer = 0.0

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float) -> None:
        self.vy += settings.GRAVITY * dt
        self.x += self.vx * dt
        self.frame_timer += dt
        
        self.x = max(0, min(self.x, settings.VIRTUAL_WIDTH - self.width))
        self.y = max(0, self.y)
        piso_y = settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT - self.height
        if self.y > piso_y:
            self.y = piso_y
            self.vy = 0

        if self.img_indx != 0:
            self.img_indx = (self.img_indx + 1) % 3
        if self.is_ghost:
            if self.power_up_timer > 0:
                self.power_up_timer -= dt
            else:
                self.is_ghost = False
                self.power_up_timer = 0
                pygame.mixer.music.load(settings.BASE_DIR / "assets" / "sounds" / "marios_way.ogg")
                pygame.mixer.music.play(loops=-1)
        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.img_indx += 1
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        if not self.is_ghost:
            surface.blit(settings.TEXTURES["bird"][self.img_indx], self.get_rect())
        else:
            img = settings.TEXTURES["ghost_bird"].copy()
            divisor = max(10, int(self.power_up_timer * 30))   
            opacidad = 175 + 80 * math.sin(pygame.time.get_ticks() / divisor)
            img.set_alpha(int(opacidad))
            surface.blit(img, self.get_rect())
