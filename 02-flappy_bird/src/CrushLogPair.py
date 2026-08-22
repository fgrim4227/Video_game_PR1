from src.LogPair import LogPair
import pygame

import settings
class CrushLogPair(LogPair):
    def __init__(self, x: float, y: float) -> None:
            super().__init__(x, y)
            self.og_pos_top = y
            self.og_pos_bottom = self.get_bottom_rect.y
            self.crush_vy = settings.LOG_CRUSH_SPEED
            self.retreat_vy = settings.LOG_RETREAT_SPEED
            self.falling = True
    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt
        top_log = self.get_top_rect()
        bottom_log = self.get_bottom_rect()
        if(bottom_log.top - top_log.bottom > 1 and self.falling):
            bottom_log.y -= self.crush_vy*dt
            top_log.y += self.crush_vy*dt
        else:
            if(self.og_pos_top - self.y > 1 and self.og_pos_bottom - bottom_log.y > 1):
                self.falling = False
                bottom_log.y += self.retreat_vy*dt
                top_log.y -= self.retreat_vy*dt
            else:
                self.falling = True
