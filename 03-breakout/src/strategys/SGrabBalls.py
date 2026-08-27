import random
import settings
from src.strategys.PwStrategy import PwStrategy

class StratGrabBalls(PwStrategy):
    def __init__(self):
        super().__init__()
        self.icon_frame = 2
    def effect(self, dt: float, play_state):
        for ball in play_state.balls:
            if ball.vy == 0:
                ball.stick_to_paddle(play_state.paddle)

    def on_input(self, input_id, input_data, play_state):
        if input_id == "shoot" and input_data.pressed:
            for ball in play_state.balls:
                if ball.vy == 0:
                    ball.unstuck(play_state.paddle, False)
                    ball.vy = random.randint(-180, -100)
                    ball.vx = play_state.paddle.vx + play_state.paddle.vx * random.randint(-20, 20) / 100