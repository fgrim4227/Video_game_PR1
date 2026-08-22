from src.Paddle import Paddle
from src.Ball import Ball
import settings
class Bot(Paddle):
    def __init__(self, x : float, y : float, width : float, height : float, ball : Ball) -> None:
        super().__init__(x, y, width, height)
        self.already_calculated : bool = False
        self.target_y : float = self.y
        self.ref_ball : Ball = ball

    def calculate_target(self, dt: float) -> None:
        curr_x = self.ref_ball.x
        curr_y = self.ref_ball.y
        curr_vx = self.ref_ball.vx
        curr_vy = self.ref_ball.vy
        b_height = self.ref_ball.height
        calc_lim = (settings.VIRTUAL_WIDTH - self.width - settings.PADDLE_X_OFFSET - self.ref_ball.width) if curr_vx > 0 else settings.PADDLE_WIDTH + settings.PADDLE_X_OFFSET
        lower_lim = settings.VIRTUAL_HEIGHT
        sim_step = 0.02
        if not self.already_calculated:
            if(curr_vx > 0):
                while curr_x <= calc_lim:
                    if(curr_y <= 0):
                        curr_y = 0
                        curr_vy *= -1
                    elif(curr_y >= lower_lim):
                        curr_y = lower_lim - b_height
                        curr_vy *= -1
                    curr_x += curr_vx * sim_step
                    curr_y += curr_vy * sim_step
                self.target_y = curr_y
                self.already_calculated = True
            elif(curr_vx < 0):
                while (curr_x >= calc_lim):
                    if(curr_y <= 0):
                        curr_y = 0
                        curr_vy *= -1
                    elif(curr_y >= lower_lim - b_height):
                        curr_y = lower_lim - b_height
                        curr_vy *= -1
                    curr_x += curr_vx * sim_step
                    curr_y += curr_vy * sim_step
                self.target_y = curr_y
                self.already_calculated = True

    def move_towards_goal(self, step : float)->None:
        if(round(self.y + self.height / 2) > self.target_y and (self.y + self.height / 2) - self.target_y > 2):
            self.y += -settings.PADDLE_SPEED * step
        elif(round(self.y + self.height / 2) < self.target_y and self.target_y - (self.y + self.height / 2) > 2):
            self.y += settings.PADDLE_SPEED * step
        if(self.y < 0):
            self.y = 0
        if(self.y >= settings.VIRTUAL_HEIGHT - self.height):
            self.y = settings.VIRTUAL_HEIGHT - (self.height)

    def update(self, dt: float) -> None:
            if(self.already_calculated):
                self.move_towards_goal(dt)
            else:
                self.calculate_target(dt)
                self.already_calculated = True

    def reset_prediction(self):
        self.already_calculated = False
        

                    

