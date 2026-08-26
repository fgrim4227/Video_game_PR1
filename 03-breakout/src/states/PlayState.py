"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""

import random
import pygame

from gale.factory import AbstractFactory
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text
from src.Missile import Missile
import settings
import src.powerups

class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])

        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")
        self.missiles = []
        
        self.active_strategies = {}

    def add_strategy(self, key: str, strategy, time: float):
        strategy.activate(time)
        self.active_strategies[key] = strategy

    def update(self, dt: float) -> None:
        self.paddle.update(dt)

        strategies_to_remove = []
        for key, strat in self.active_strategies.items():
            strat.update(dt, self)
            if not strat.active:
                strategies_to_remove.append(key)
                
        for key in strategies_to_remove:
            del self.active_strategies[key]

        ball_dt = dt
        if "slow_time" in self.active_strategies and self.active_strategies["slow_time"].slowing:
            ball_dt *= 0.2

        has_grab = "grab_balls" in self.active_strategies
        
        for ball in self.balls:
            current_ball_dt = dt if ball.vy == 0 else ball_dt
            ball.update(current_ball_dt)
            ball.solve_world_boundaries()

            if ball.collides(self.paddle):
                if not has_grab:  
                    if ball.vy == 0:
                        ball.unstuck(self.paddle, False)
                        ball.vy = random.randint(-180, -100)
                        ball.vx = settings.PADDLE_SPEED * random.randint(-120, 120) / 100  
                    
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)
                else:
                    ball.stick_to_paddle(self.paddle)
            
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())
            if brick is None:
                continue
            
            self.score += brick.score()
            brick.hit()
            ball.rebound(brick)

            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(self.powerups_abstract_factory.get_factory("TwoMoreBall").create(r.centerx - 8, r.centery - 8))
            elif random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(self.powerups_abstract_factory.get_factory("GrabBalls").create(r.centerx -8, r.centery - 8))
            elif random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(self.powerups_abstract_factory.get_factory("MissilesBall").create(r.centerx -8, r.centery - 8))
            elif random.random() < 0.3:
                r = brick.get_collision_rect()
                self.powerups.append(self.powerups_abstract_factory.get_factory("SlowDownTime").create(r.centerx -8, r.centery - 8))

        self.balls = [ball for ball in self.balls if ball.active]
        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        for powerup in self.powerups:
            powerup.update(dt)
            if powerup.collides(self.paddle):
                powerup.take(self)

        self.powerups = [p for p in self.powerups if p.active]

        if self.brickset.size == 1 and next((True for _, b in self.brickset.bricks.items() if b.broken), False):
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120
        i = 0
        while i < self.lives:
            surface.blit(settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0])
            heart_x += 11
            i += 1
        while i < 3:
            surface.blit(settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1])
            heart_x += 11
            i += 1

        render_text(surface, f"Score: {self.score}", settings.FONTS["tiny"], settings.VIRTUAL_WIDTH - 80, 5, (255, 255, 255))
        
        self.brickset.render(surface)
        self.paddle.render(surface)

        for ball in self.balls:
            ball.render(surface)
        for powerup in self.powerups:
            powerup.render(surface)
        for m in self.missiles:
            m.render(surface)

        ui_x = 10 
        ui_y = 5
        icon_map = {"grab_balls": 2, "missil": 3, "slow_time": 4}

        for key, strat in self.active_strategies.items():
            if key not in icon_map:
                continue 
            if(key == "slow_time"):
                if 0 <= strat.window_timer <= 2.0 and strat.can_slow:
                    if (pygame.time.get_ticks() // 200) % 2 == 0:
                            continue
                elif(strat.slowing and 0 <= strat.timer <= 2):
                    if (pygame.time.get_ticks() // 200) % 2 == 0:
                            continue
            elif strat.timer < 2.0:
                if (pygame.time.get_ticks() // 200) % 2 == 0:
                    continue 
            surface.blit(
                settings.TEXTURES["spritesheet"],
                (ui_x, ui_y),
                settings.FRAMES["powerups"][icon_map[key]]
            )
            if hasattr(strat, 'max_time') and strat.max_time > 0:
                if hasattr(strat, "window_timer") and strat.can_slow:
                    ratio = max(0, strat.window_timer / strat.max_time)
                else:
                    ratio = max(0, strat.timer / strat.max_time)
                bar_width = int(16 * ratio)
                
                pygame.draw.rect(surface, (255, 50, 50), (ui_x, ui_y + 18, bar_width, 3))
                pygame.draw.rect(surface, (255, 255, 255), (ui_x, ui_y + 18, 16, 3), 1)

            ui_x += 24

    def on_input(self, input_id: str, input_data: InputData) -> None:
        for strat in self.active_strategies.values():
            strat.on_input(input_id, input_data, self)
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
                missiles = self.missiles
            )