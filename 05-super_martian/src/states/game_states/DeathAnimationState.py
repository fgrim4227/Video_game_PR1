import pygame
from gale.state import BaseState
from gale.timer import Timer
import settings
from gale.text import render_text
class DeathAnimationState(BaseState):
    def enter(self, **enter_params) -> None:
        self.player = enter_params["player"]
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params["game_level"]
        self.camera = enter_params["camera"]
        self.score = enter_params["score"]
        self.last_time = enter_params["last_time"]
        pygame.mixer.music.stop()
        settings.SOUNDS["loose_life"].play()

        self.player.frame_index = 4
        self.fade_alpha = 0
        Timer.tween(
            0.5,
            [(self.player, {"y": self.player.y - 50})],
            ease_function_name="out_cubic",
            on_finish=self._fall_down
        )

    def _fall_down(self):
        Timer.tween(
            1.0,
            [(self.player, {"y": settings.VIRTUAL_HEIGHT + 50})],
            ease_function_name="in_cubic",
            on_finish= self.trasition_out       
        )
    def trasition_out(self):
        Timer.tween(
            1, 
            [(self, {"fade_alpha": 255})],
            on_finish=lambda: self.state_machine.change(
                "dead_screen", 
                player=self.player, 
                level=self.level
            )
        )
    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        self.player.render(surface, self.camera)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.last_time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
            shadowed=True,
        )
        if hasattr(self, 'fade_alpha') and self.fade_alpha > 0:
            fade_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(int(self.fade_alpha))
            surface.blit(fade_surface, (0, 0))