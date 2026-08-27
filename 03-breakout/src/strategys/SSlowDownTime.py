from src.strategys.PwStrategy import PwStrategy
import pygame
import settings
class StratSlowTime(PwStrategy):
    def __init__(self):
        super().__init__()
        self.can_slow = True
        self.slowing = False
        self.window_timer = 10
        self.icon_frame = 4

    def activate(self, window_time: float):
        self.window_timer = window_time
        self.max_time = 6
        self.max_window_timer = window_time
        self.active = True
        self.can_slow = True
        self.slowing = False
        self.timer = 6

    def update(self, dt: float, play_state):
        if self.can_slow:
            self.window_timer -= dt
            if self.window_timer <= 0:
                self.active = False
        elif self.slowing:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False
                self.slowing = False

    def on_input(self, input_id, input_data, play_state):
        if self.can_slow and input_id == "slow_t" and input_data.pressed:
            self.slowing = True
            self.can_slow = False
            self.timer = 5
    def render_ui(self, surface: pygame.Surface, x: int, y: int) -> int:
        is_blinking = False
        
        if self.can_slow and 0 <= self.window_timer <= 2.0:
            is_blinking = (pygame.time.get_ticks() // 200) % 2 == 0
        elif self.slowing and 0 <= self.timer <= 2.0:
            is_blinking = (pygame.time.get_ticks() // 200) % 2 == 0
            
        if not is_blinking:
            surface.blit(
                settings.TEXTURES["spritesheet"], (x, y), settings.FRAMES["powerups"][self.icon_frame]
            )
            
            ratio = 0
            if self.can_slow and self.window_timer > 0:
                ratio = max(0, self.window_timer / self.max_window_timer)
            elif self.slowing and self.max_time > 0:
                ratio = max(0, self.timer / self.max_time)
                
            bar_width = int(16 * ratio)
            pygame.draw.rect(surface, (255, 50, 50), (x, y + 18, bar_width, 3))
            pygame.draw.rect(surface, (255, 255, 255), (x, y + 18, 16, 3), 1)

        return x + 24