from src.strategys.PwStrategy import PwStrategy

class StratSlowTime(PwStrategy):
    def __init__(self):
        super().__init__()
        self.can_slow = True
        self.slowing = False
        self.window_timer = 10

    def activate(self, window_time: float):
        self.window_timer = window_time
        self.max_time = window_time
        self.active = True
        self.can_slow = True
        self.slowing = False
        self.timer = window_time

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