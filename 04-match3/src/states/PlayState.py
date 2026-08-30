"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.PowerUp import Powerup

class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = int(self.level * 1.3 * 1000)

        self.dragging = False
        self.dragging_tile = None
        self.og_x = 0
        self.og_y = 0
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.drag_axis = None
        self.done_dynamic = True
    
        self.hint_tile_pos = None
        self.hint_action_id = 0
        self._reset_hint_timer()

        self.is_resetting = False
        self.show_reset_text = False
        self.reset_timer_blink = None
        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )
        def decrement_timer():
            if not self.is_resetting:
                self.timer -= 1

                if self.timer <= 5:
                    settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)
        self.hint_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.hint_alpha_surface,
            (255, 215, 0, 255), 
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
            width=4
        )
    def follow_mouse(self):
        if self.dragging and self.dragging_tile:
            m_x, m_y = pygame.mouse.get_pos()
            m_x = m_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            m_y = m_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            dx = m_x - self.start_mouse_x
            dy = m_y - self.start_mouse_y

            if abs(dx) > 5 or abs(dy) > 5:
                self.drag_axis = 'x' if abs(dx) > abs(dy) else 'y'

            clamped_dx, clamped_dy = 0, 0
            if self.drag_axis == 'x':
                min_x = -settings.TILE_SIZE if self.highlighted_j1 > 0 else 0
                max_x = settings.TILE_SIZE if self.highlighted_j1 < settings.BOARD_WIDTH - 1 else 0
                clamped_dx = max(min_x, min(max_x, dx))
            elif self.drag_axis == 'y':
                min_y = -settings.TILE_SIZE if self.highlighted_i1 > 0 else 0
                max_y = settings.TILE_SIZE if self.highlighted_i1 < settings.BOARD_HEIGHT - 1 else 0
                clamped_dy = max(min_y, min(max_y, dy))

            self.dragging_tile.x = self.og_x + clamped_dx
            self.dragging_tile.y = self.og_y + clamped_dy
    def _calculate_matches(self, tiles_to_check: List[Any]) -> None:
        matches = self.board.calculate_matches_for(tiles_to_check)

        if matches is None:
            self.active = True
            self.done_dynamic = True
            self._reset_hint_timer()
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        pending_powerups = []
        extra_tiles_to_destroy = set()

        for match in matches:
            self.score += len(match) * 50
            match_len = len(match)
            
            for tile in match:
                if isinstance(tile, Powerup):
                    destroyed = tile.activate(self.board)
                    extra_tiles_to_destroy.update(destroyed)
            
            if match_len >= 4:
                target_tile = next((t for t in match if getattr(t, 'moved', False)), match[0])
                size_key = min(match_len, 5) 
                pending_powerups.append({
                    "i": target_tile.i,
                    "j": target_tile.j,
                    "color": target_tile.color,
                    "variety": target_tile.variety,
                    "size": size_key
                })

        self.score += len(extra_tiles_to_destroy) * 50

        self.board.remove_matches()

        for t in extra_tiles_to_destroy:
            self.board.tiles[t.i][t.j] = None

        for pu_data in pending_powerups:
            new_pu = Powerup(
                pu_data["i"], pu_data["j"], pu_data["color"], 
                pu_data["variety"], pu_data["size"]
            )
            self.board.tiles[pu_data["i"]][pu_data["j"]] = new_pu

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches([item[0] for item in falling_tiles]),
        )
    def _reset_hint_timer(self) -> None:
        self.hint_action_id += 1
        self.hint_tile_pos = None
        current_id = self.hint_action_id

        Timer.after(10, lambda: self._show_hint(current_id))

    def _show_hint(self, action_id: int) -> None:
        if self.hint_action_id == action_id and self.active and self.done_dynamic:
            self.hint_tile_pos = self.board.get_possible_move()
    def _start_board_reset(self) -> None:
        self.is_resetting = True
        self.show_reset_text = True
        self.active = False
        self.done_dynamic = False

        def toggle_text():
            self.show_reset_text = not self.show_reset_text

        self.reset_timer_blink = Timer.every(0.25, toggle_text)

        def finalize_reset():
            self.reset_timer_blink.remove()
            self.board.reset()
            self.is_resetting = False
            self.active = True
            self.done_dynamic = True

        Timer.after(2.0, finalize_reset)
    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            #Paso goal_score pq al ganar con power up acumula mucho
            #Hace que siguiente nivel sea casi instantaneo
            self.state_machine.change("begin", level=self.level + 1, score=self.goal_score)
        self.follow_mouse()
        if self.done_dynamic and not self.is_resetting:
            if not self.board.has_possible_moves():
                powerups = self.board.get_available_powerup()
                if powerups:
                    pw_to_activate = powerups[0]
                    self._auto_activate_powerup(pw_to_activate)
                else:
                    self._start_board_reset()
    def _auto_activate_powerup(self, powerup: Any) -> None:
        self.active = False
        self.done_dynamic = False
        tiles_to_destroy = set()
        activated_pw = set()
        pw_to_activate = []

        pw_to_activate.append(powerup)

        while(pw_to_activate):
            current_pw = pw_to_activate.pop()
            tiles_to_destroy.update(current_pw.activate(self.board))
            for tile in tiles_to_destroy:
                if tile in activated_pw:
                    continue
                elif isinstance(tile, Powerup):
                    pw_to_activate.append(tile)
                    activated_pw.add(tile)

        if tiles_to_destroy:
            for t in tiles_to_destroy:
                self.score += 50
                self.board.tiles[t.i][t.j] = None
            settings.SOUNDS["match"].play()
            falling_tiles = self.board.get_falling_tiles()
            Timer.tween(
                0.25,
                falling_tiles,
                on_finish=lambda: self._calculate_matches([item[0] for item in falling_tiles])
            )
        else:
            self.active = True
            self.done_dynamic = True

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.dragging and self.dragging_tile:
            self.dragging_tile.render(surface, self.board.x, self.board.y)

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )
        if self.hint_tile_pos is not None and not self.dragging:
            import math
            hi, hj = self.hint_tile_pos
            x = hj * settings.TILE_SIZE + self.board.x
            y = hi * settings.TILE_SIZE + self.board.y
            alpha = int(abs(math.sin(pygame.time.get_ticks() / 200.0)) * 200) + 55
            self.hint_alpha_surface.set_alpha(alpha)
            
            surface.blit(self.hint_alpha_surface, (x, y))
        if self.is_resetting and self.show_reset_text:
            render_text(
                surface,
                "No More Moves!",
                settings.FONTS["large"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2 - 24,
                (255, 99, 99),
                center=True,
                shadowed=True,
            )
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return
        if input_id == "click":
            self._reset_hint_timer()
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            if input_data.pressed:
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE

                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                    self.dragging = True
                    self.dragging_tile = self.board.tiles[i][j]
                    self.dragging_tile.moved = True
                    self.og_x = self.dragging_tile.x
                    self.og_y = self.dragging_tile.y
                    self.start_mouse_x = pos_x
                    self.start_mouse_y = pos_y
                    self.drag_axis = None
                    self.highlighted_i1 = i
                    self.highlighted_j1 = j
                    self.highlighted_tile = True

            elif input_data.released and self.dragging:
                self.dragging = False
                self.highlighted_tile = False

                target_i = round((self.dragging_tile.y) / settings.TILE_SIZE)
                target_j = round((self.dragging_tile.x) / settings.TILE_SIZE)

                di = abs(target_i - self.highlighted_i1)
                dj = abs(target_j - self.highlighted_j1)
                if di == 0 and dj == 0:
                    if isinstance(self.dragging_tile, Powerup):
                        if isinstance(self.dragging_tile, Powerup):
                            self.active = False

                            tiles_to_destroy = set()
                            powerups_to_activate = [self.dragging_tile]
                            activated = set()

                            while powerups_to_activate:
                                current_pu = powerups_to_activate.pop(0)
                                if current_pu in activated:
                                    continue
                                activated.add(current_pu)

                                destroyed = current_pu.activate(self.board)
                                for t in destroyed:
                                    tiles_to_destroy.add(t)
                                    board_tile = self.board.tiles[t.i][t.j]
                                    if isinstance(board_tile, Powerup) and board_tile not in activated:
                                        powerups_to_activate.append(board_tile)
                        
                        if tiles_to_destroy:
                            self.score += len(tiles_to_destroy) * 50
                            for t in tiles_to_destroy:
                                self.board.tiles[t.i][t.j] = None
                            
                            settings.SOUNDS["match"].play()
                            falling_tiles = self.board.get_falling_tiles()
                            Timer.tween(
                                0.25,
                                falling_tiles,
                                on_finish=lambda: self._calculate_matches([item[0] for item in falling_tiles])
                            )
                        else:
                            self.active = True
                    else:
                        self.dragging_tile.moved = False

                if (di == 1 and dj == 0) or (di == 0 and dj == 1):
                    self.active = False
                    tile1 = self.dragging_tile
                    tile2 = self.board.tiles[target_i][target_j]

                    def arrive():
                        self.done_dynamic = False
                        self.board.tiles[tile1.i][tile1.j], self.board.tiles[tile2.i][tile2.j] = (
                            self.board.tiles[tile2.i][tile2.j],
                            self.board.tiles[tile1.i][tile1.j],
                        )
                        tile1.i, tile1.j, tile2.i, tile2.j = tile2.i, tile2.j, tile1.i, tile1.j

                        matches = self.board.calculate_matches_for([tile1, tile2])

                        if matches is None:
                            self.board.tiles[tile1.i][tile1.j], self.board.tiles[tile2.i][tile2.j] = (
                                self.board.tiles[tile2.i][tile2.j],
                                self.board.tiles[tile1.i][tile1.j],
                            )
                            tile1.i, tile1.j, tile2.i, tile2.j = tile2.i, tile2.j, tile1.i, tile1.j
                            self.dragging_tile.moved = False
                            settings.SOUNDS["error"].play()
                            Timer.tween(
                                0.15,
                                [
                                    (tile1, {"x": self.og_x, "y": self.og_y}),
                                    (tile2, {"x": tile2.j * settings.TILE_SIZE, "y": tile2.i * settings.TILE_SIZE}),
                                ],
                                on_finish=lambda: setattr(self, "active", True),
                            )
                            self.dragging_tile = None
                        else:
                            self.board.matches = [] 
                            self._calculate_matches([tile1, tile2])
                            
                            self.dragging_tile = None
                    Timer.tween(
                        0.15,
                        [
                            (tile1, {"x": tile2.j * settings.TILE_SIZE, "y": tile2.i * settings.TILE_SIZE}),
                            (tile2, {"x": self.og_x, "y": self.og_y}),
                        ],
                        on_finish=arrive,
                    )
                else:
                    Timer.tween(
                        0.15,
                        [(self.dragging_tile, {"x": self.og_x, "y": self.og_y})]
                    )
        '''            
        if input_id == "reset" and input_data.pressed:
            self.board.change_state()
            self._reset_hint_timer()
        '''