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

        self.goal_score = self.level * 1.25 * 1000

        self.dragging = False
        self.dragging_tile = None
        self.og_x = 0
        self.og_y = 0
        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.drag_axis = None
        self.done_dynamic = True
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

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)
    def follow_mouse(self):
        if self.dragging and self.dragging_tile:
            m_x, m_y = pygame.mouse.get_pos()
            m_x = m_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            m_y = m_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            dx = m_x - self.start_mouse_x
            dy = m_y - self.start_mouse_y

            if self.drag_axis is None:
                if abs(dx) > 5 or abs(dy) > 5:
                    self.drag_axis = 'x' if abs(dx) > abs(dy) else 'y'

            clamped_dx, clamped_dy = 0, 0
            #if self.drag_axis == 'x':
            min_x = -settings.TILE_SIZE if self.highlighted_j1 > 0 else 0
            max_x = settings.TILE_SIZE if self.highlighted_j1 < settings.BOARD_WIDTH - 1 else 0
            clamped_dx = max(min_x, min(max_x, dx))
            #elif self.drag_axis == 'y':
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
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            self.score += len(match) * 50

        self.board.remove_matches()
        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches([item[0] for item in falling_tiles]),
        )
    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)
        self.follow_mouse()
        if self.done_dynamic:
            if not (self.board.has_possible_moves()):
                self.board.reset()
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
    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return
        if input_id == "click":
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT

            if input_data.pressed:
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE

                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                    self.dragging = True
                    self.dragging_tile = self.board.tiles[i][j]
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

                            settings.SOUNDS["error"].play()
                            Timer.tween(
                                0.15,
                                [
                                    (tile1, {"x": self.og_x, "y": self.og_y}),
                                    (tile2, {"x": tile2.j * settings.TILE_SIZE, "y": tile2.i * settings.TILE_SIZE}),
                                ],
                                on_finish=lambda: setattr(self, "active", True),
                            )
                        else:
                            settings.SOUNDS["match"].stop()
                            settings.SOUNDS["match"].play()
                            for match in matches:
                                self.score += len(match) * 50

                            self.board.remove_matches()
                            falling_tiles = self.board.get_falling_tiles()
                            Timer.tween(
                                0.25,
                                falling_tiles,
                                on_finish=lambda: self._calculate_matches([item[0] for item in falling_tiles]),
                            )
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

                self.dragging_tile = None
        if(input_id == "reset" and input_data.pressed):
            self.board.reset()