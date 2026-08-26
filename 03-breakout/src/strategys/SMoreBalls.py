import random
import settings
from gale.factory import Factory
from src.Ball import Ball
from src.strategys.PwStrategy import PwStrategy

class StratMoreBalls(PwStrategy):
    def __init__(self):
        super().__init__()
        self.ball_factory = Factory(Ball)

    def effect(self, dt: float, play_state):
        paddle = play_state.paddle
        for _ in range(2):
            b = self.ball_factory.create(paddle.x + paddle.width // 2 - 4, paddle.y - 8)
            settings.SOUNDS["paddle_hit"].stop()
            settings.SOUNDS["paddle_hit"].play()
            b.vx = random.randint(-80, 80)
            b.vy = random.randint(-170, -100)
            play_state.balls.append(b)
            
        self.active = False