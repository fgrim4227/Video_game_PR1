from src.LogPair import LogPair
import pygame

import settings
class CrushLogPair(LogPair):
    def __init__(self, x: float, y: float, log_gap = settings.LOGS_GAP) -> None:
        super().__init__(x, y, log_gap)
        self.current_gap = log_gap
        self.crush_vy = settings.LOG_CRUSH_SPEED
        self.retreat_vy = settings.LOG_RETREAT_SPEED
        self.falling = True

    def get_bottom_rect(self) -> pygame.Rect:
        return pygame.Rect(
            round(self.x),
            round(self.y + self.current_gap + settings.LOG_HEIGHT),
            settings.LOG_WIDTH,
            settings.LOG_HEIGHT,
        )

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.falling:
            self.y += self.crush_vy * dt
            self.current_gap -= (self.crush_vy * 2) * dt           
            if self.current_gap <= 1:
                settings.SOUNDS["crash_logs"].play()
                self.falling = False
        else:
            self.y -= self.retreat_vy * dt
            self.current_gap += (self.retreat_vy * 2) * dt
            if self.current_gap >= self.logs_gap:
                self.falling = True