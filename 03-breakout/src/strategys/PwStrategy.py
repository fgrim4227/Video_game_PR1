class PwStrategy:
    def __init__(self):
        self.active = False
        self.timer = 0

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

    def on_input(self, input_id, input_data, play_state):
        pass
    def render(self, surface, play_state):
        pass