"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player
from src.FlyingCreature import FlyingCreature

class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.active = False

        self.fade_alpha = 255
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)
        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        if self.player is None:
            # Resting exactly on the ground tile's surface (row 9, one tile
            # below the platform's top edge) rather than a few pixels into
            # it, so gale.tilemap's one-way platform collision (which
            # requires the entity to already be at/above the surface) picks
            # it up on the very first frame instead of falling through.
            spawn_y = 9 * self.tilemap.tile_height - 20
            self.player = Player(0, spawn_y, self.game_level)
            self.player.change_state("idle")

        self.player.lives = enter_params.get("lives", 3)

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.follow(self.player, rate=settings.CAMERA_FOLLOW_RATE)
            self.camera.bounds = self.game_level.get_rect()
            self.camera.x, self.camera.y = self.player.x, self.player.y
            self.camera.update(0)

        self.clock = enter_params.get("clock")

        if self.clock is None:
            self.clock = Clock(180)

            def countdown_timer():
                if not (self.clock.paused):
                    self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")

            Timer.every(1, countdown_timer)
        else:
            Timer.resume()
        self.clock.paused = True
        self.TARGET_SCORE = 300 + (300 * 0.2 * self.level)

        Timer.tween(3, [(self, {"fade_alpha": 0})], on_finish=self.activate)

    def activate(self):
        self.active = True
        self.clock.paused = False
    def update(self, dt: float) -> None:
        if(self.active):   
            if self.player.is_dead:          
                pygame.mixer.music.stop()           
                pygame.mixer.music.unload()          
                Timer.clear()          
                self.state_machine.change("death_animation_state", player=self.player, level=self.level, game_level = self.game_level, camera = self.camera, last_time = self.clock.time, score = self.player.score)           

            player_rect = self.player.get_collision_rect()          
            for block in self.game_level.special_blocks:           
                if not block["hit"]:           
                    block_rect = pygame.Rect(block["x"], block["y"], block["width"], block["height"] + 10)           
                    if player_rect.colliderect(block_rect):           
                        if self.player.vy < 0:          
                            if self.player.score >= self.TARGET_SCORE:          
                                block["hit"] = True          
                                settings.SOUNDS["hit_block"].play()           
                                self._spawn_key(block["x"], block["y"] - 4)           
            self.player.update(dt)
         
            if self.player.y >= self.tilemap.pixel_height:           
                self.player.change_state("dead")      

            self.camera.update(dt)          
            self.game_level.update(dt)
          
            for creature in self.game_level.creatures:          
                if self.player.collides(creature):          
                    pr = self.player.get_collision_rect()          
                    cr = creature.get_collision_rect()            
                    intersection = self.player.get_intersection(pr, cr)          
                    if intersection is not None:          
                        shift_x, shift_y = intersection          
                        min_shift = min(abs(shift_x), abs(shift_y))           
                        if min_shift == (abs(shift_y)) and self.player.vy > 0:          
                            settings.SOUNDS["jump"].play()          
                            if self.player.jump_held:          
                                self.player.vy = -settings.JUMP_TAKEOFF_SPEED          
                            else:       
                                self.player.vy = -settings.JUMP_TAKEOFF_SPEED + 0.5 * settings.JUMP_TAKEOFF_SPEED            
                            if not getattr(creature, 'is_dying', False):            
                                creature.is_dying = True
                                if isinstance(creature, FlyingCreature):           
                                    creature.change_state("fall")
                                    self.player.score += 50          
                                else:           
                                    creature.change_state("dead", flipped=creature.flipped)   
                                    self.player.score += 20        
                            else:          
                                self.player.score += 5           
                        else:           
                            if not getattr(creature, 'is_dying', False) and not (creature.is_dead):           
                                self.player.change_state("dead")
            
            for item in self.game_level.items:           
                if not item.active or not item.collidable:            
                    continue           
                if self.player.collides(item):           
                    item.on_collide(self.player)           
                    item.on_consume(self.player)

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        for block in self.game_level.special_blocks:
            if block["hit"]:
                empty_block_img = settings.FRAMES["tiles"][69] 

                rect = self.camera.apply(pygame.Rect(block["x"], block["y"], block["width"], block["height"]))
                
                surface.blit(settings.TEXTURES["tiles"], (rect.x, rect.y), empty_block_img)

        self.player.render(surface, self.camera)

        render_text(
            surface,
            f"Score: {self.player.score} / {int(self.TARGET_SCORE)}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
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

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
        else:
            self.player.on_input(input_id, input_data)

    def _spawn_key(self, x, y):
            from src.GameItem import GameItem
            from gale.timer import Timer
            key = GameItem(
                x, y, 16, 16, "tiles", 68, 
                collidable=True, consumable=True, 
                on_consume=self._win_level
            )
            Timer.tween(
                1.5, 
                [(key, {"y": y - 16})], 
                ease_function_name= "linear"
            )
            self.game_level.items.append(key)

    def _win_level(self, item, player):

        settings.SOUNDS["key_obtain"].play()
        for game_item in self.game_level.items:
            game_item.collidable = False

        self.state_machine.change("victory", game_level = self.game_level, player = self.player, camera = self.camera, clock = self.clock, level=self.level )
