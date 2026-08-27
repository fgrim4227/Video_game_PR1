import settings
import pygame
class PwStrategy:
    def __init__(self):
        self.active = False
        self.timer = 0
        self.max_time = 0
        self.icon_frame = None

    def activate(self, time: float):
        self.timer = time
        self.max_time = time
        self.active = True

    def update(self, dt: float, play_state):
        if self.active:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False
        self.effect(dt, play_state)

    def effect(self, dt: float, play_state):
        pass
    def render(self, surface, play_state):
        pass
    def on_input(self, input_id, input_data, play_state):
        pass
    def render_ui(self, surface: pygame.Surface, x: int, y: int) -> int:
        if self.icon_frame is None:
            return x 
        is_blinking = self.timer < 2.0 and (pygame.time.get_ticks() // 200) % 2 == 0
        if not is_blinking:
            surface.blit(
                settings.TEXTURES["spritesheet"],
                (x, y),
                settings.FRAMES["powerups"][self.icon_frame]
            )
            if hasattr(self, 'max_time') and self.max_time > 0:
                ratio = max(0, self.timer / self.max_time)
                bar_width = int(16 * ratio)
                pygame.draw.rect(surface, (255, 50, 50), (x, y + 18, bar_width, 3))
                pygame.draw.rect(surface, (255, 255, 255), (x, y + 18, 16, 3), 1)
        return x + 24