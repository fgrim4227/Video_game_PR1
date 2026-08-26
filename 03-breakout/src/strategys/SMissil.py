from src.Missile import Missile
from src.strategys.PwStrategy import PwStrategy

class StratMissil(PwStrategy):
    def update(self, dt: float, play_state):
        if self.active:
            self.timer -= dt         
        self.effect(dt, play_state)
        if self.timer <= 0 and len(play_state.missiles) == 0:
            self.active = False
    def effect(self, dt: float, play_state):
        for missil in play_state.missiles:
            missil.update(dt)
            if not missil.collides(play_state.brickset):
                continue
            
            brick = play_state.brickset.get_colliding_brick(missil.get_collision_rect())
            if brick is None:
                continue 
                
            score_destruction = 0
            while not brick.broken:
                score_destruction += brick.score()
                brick.hit()
            play_state.score += score_destruction
        play_state.missiles = [r for r in play_state.missiles if r.active]

    def on_input(self, input_id, input_data, play_state):
        if input_id == "missil" and input_data.pressed:
            if len(play_state.missiles) == 0:
                play_state.missiles.append(Missile(play_state.paddle.x, play_state.paddle.y))
                play_state.missiles.append(Missile(play_state.paddle.x + play_state.paddle.width - 4, play_state.paddle.y))