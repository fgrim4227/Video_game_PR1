"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Board.
"""

from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from gale.timer import Timer
from gale.text import render_text
from src.Tile import Tile


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.matches: List[List[Tile]] = []
        self.tiles: List[List[Tile]] = []
        self.test_case = 0 

        self.test_cases_funcs = {
            0: self._generate_normal,
            1: self._generate_case_1,
            2: self._generate_case_2,
            3: self._generate_case_3,
            4: self._generate_case_4
        }
        self._initialize_tiles()

    def render(self, surface: pygame.Surface) -> None:
        for row in self.tiles:
            for tile in row:
                tile.render(surface, self.x, self.y)

    def _is_match_generated(self, i: int, j: int, color: int) -> bool:
        if (
            i >= 2
            and self.tiles[i - 1][j].color == color
            and self.tiles[i - 2][j].color == color
        ):
            return True

        return (
            j >= 2
            and self.tiles[i][j - 1].color == color
            and self.tiles[i][j - 2].color == color
        )
    
    def get_available_powerup(self) -> Optional[Any]:
        power_ups = []
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                tile = self.tiles[i][j]
                if tile is not None and hasattr(tile, "activate"):
                    power_ups.append(tile)
        if len(power_ups) == 0:
            return None
        else:
            return power_ups
    
    def _initialize_tiles(self) -> None:
        self.test_cases_funcs[0]()

    def reset(self):
        self.matches = []
        self.tiles = []
        self.test_cases_funcs[0]()
    
    def change_state(self):
        self.matches = []
        self.tiles = []
        self.test_case = (self.test_case + 1) % 5
        self.test_cases_funcs[self.test_case]()

    def _generate_normal(self) -> None:
        self.tiles = [[None for _ in range(settings.BOARD_WIDTH)] for _ in range(settings.BOARD_HEIGHT)]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                color = random.randint(0, settings.NUM_COLORS - 1)
                while self._is_match_generated(i, j, color):
                    color = random.randint(0, settings.NUM_COLORS - 1)
                self.tiles[i][j] = Tile(i, j, color, random.randint(0, settings.NUM_VARIETIES - 1))

    def _generate_case_1(self) -> None:
        self._generate_normal()
        self.tiles[0][0].color = 0
        self.tiles[0][1].color = 0
        self.tiles[0][2].color = 1
        self.tiles[1][2].color = 0
        self.tiles[0][3].color = 0

        self.tiles[3][3].color = 5
        self.tiles[3][4].color = 5
        self.tiles[2][5].color = 5
        self.tiles[3][5].color = 0
        self.tiles[3][6].color = 5
        self.tiles[3][7].color = 5

    def _generate_case_2(self) -> None:
        self._generate_normal()
        from src.PowerUp import Powerup
        color_compartido = 5
        self.tiles[1][2] = Powerup(1, 2, color_compartido, 0, 4)
        self.tiles[1][5] = Powerup(1, 5, color_compartido, 0, 5)

    def _generate_case_3(self) -> None:
        from src.PowerUp import Powerup
        self.tiles = [[None for _ in range(settings.BOARD_WIDTH)] for _ in range(settings.BOARD_HEIGHT)]

        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                if i % 2 == 0:
                    color = 0 if j % 2 == 0 else 1
                else:
                    color = 2 if j % 2 == 0 else 3
                self.tiles[i][j] = Tile(i, j, color, 0)

        self.tiles[0][0].color = 6
        self.tiles[0][1].color = 6
        self.tiles[0][2].color = 7 
        self.tiles[1][2].color = 6 

        self.tiles[2][2] = Powerup(2, 2, 4, 0, 4)
        self.tiles[5][5] = Powerup(5, 5, 5, 0, 5)
    def _generate_case_4(self) -> None:
        self._generate_normal()
        from src.PowerUp import Powerup

        trigger_color = 3

        self.tiles[3][3] = Powerup(3, 3, trigger_color, 0, 5)

        self.tiles[1][1] = Powerup(1, 1, trigger_color, 0, 4)
        self.tiles[1][6] = Powerup(1, 6, trigger_color, 0, 4)
        self.tiles[6][1] = Powerup(6, 1, trigger_color, 0, 4)
        self.tiles[6][6] = Powerup(6, 6, trigger_color, 0, 4)

        self.tiles[1][3] = Powerup(1, 3, 1, 0, 4)
        self.tiles[6][3] = Powerup(6, 3, 2, 0, 4)
        self.tiles[3][1] = Powerup(3, 1, 4, 0, 4)
        self.tiles[3][6] = Powerup(3, 6, 0, 0, 4)
    def get_possible_move(self) -> Optional[Tuple[int, int]]:
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):

                if j < settings.BOARD_WIDTH - 1:
                    self.tiles[i][j], self.tiles[i][j+1] = self.tiles[i][j+1], self.tiles[i][j]
                    has_match = self.has_match_at(i, j) or self.has_match_at(i, j+1)
                    self.tiles[i][j], self.tiles[i][j+1] = self.tiles[i][j+1], self.tiles[i][j]
                    if has_match:
                        return (i, j)

                if i < settings.BOARD_HEIGHT - 1:
                    self.tiles[i][j], self.tiles[i+1][j] = self.tiles[i+1][j], self.tiles[i][j]
                    has_match = self.has_match_at(i, j) or self.has_match_at(i+1, j)
                    self.tiles[i][j], self.tiles[i+1][j] = self.tiles[i+1][j], self.tiles[i][j]
                    if has_match:
                        return (i, j)
                        
        return None
    def has_match_at(self, i: int, j: int) -> bool:
        if self.tiles[i][j] is None:
            return False
            
        color = self.tiles[i][j].color

        h_count = 1
        for col in range(j - 1, -1, -1):
            if self.tiles[i][col] and self.tiles[i][col].color == color:
                h_count += 1
            else: break
            
        for col in range(j + 1, settings.BOARD_WIDTH):
            if self.tiles[i][col] and self.tiles[i][col].color == color:
                h_count += 1
            else: break
            
        if h_count >= 3:
            return True

        v_count = 1
        for row in range(i - 1, -1, -1):
            if self.tiles[row][j] and self.tiles[row][j].color == color:
                v_count += 1
            else: break
            
        for row in range(i + 1, settings.BOARD_HEIGHT):
            if self.tiles[row][j] and self.tiles[row][j].color == color:
                v_count += 1
            else: break
            
        return v_count >= 3

    def has_possible_moves(self) -> bool:
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):

                if j < settings.BOARD_WIDTH - 1:
                    self.tiles[i][j], self.tiles[i][j+1] = self.tiles[i][j+1], self.tiles[i][j]

                    has_match = self.has_match_at(i, j) or self.has_match_at(i, j+1)

                    self.tiles[i][j], self.tiles[i][j+1] = self.tiles[i][j+1], self.tiles[i][j]
                    
                    if has_match:
                        return True

                if i < settings.BOARD_HEIGHT - 1:
                    self.tiles[i][j], self.tiles[i+1][j] = self.tiles[i+1][j], self.tiles[i][j]

                    has_match = self.has_match_at(i, j) or self.has_match_at(i+1, j)

                    self.tiles[i][j], self.tiles[i+1][j] = self.tiles[i+1][j], self.tiles[i][j]
                    
                    if has_match:
                        return True
                        
        return False
    def _calculate_match_rec(self, tile: Tile) -> Set[Tile]:
        if tile in self.in_stack:
            return []

        self.in_stack.add(tile)

        color_to_match = tile.color

        ## Check horizontal match
        h_match: List[Tile] = []

        # Check left
        if tile.j > 0:
            left = max(0, tile.j - 2)
            for j in range(tile.j - 1, left - 1, -1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        # Check right
        if tile.j < settings.BOARD_WIDTH - 1:
            right = min(settings.BOARD_WIDTH - 1, tile.j + 2)
            for j in range(tile.j + 1, right + 1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        ## Check vertical match
        v_match: List[Tile] = []

        # Check top
        if tile.i > 0:
            top = max(0, tile.i - 2)
            for i in range(tile.i - 1, top - 1, -1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        # Check bottom
        if tile.i < settings.BOARD_HEIGHT - 1:
            bottom = min(settings.BOARD_HEIGHT - 1, tile.i + 2)
            for i in range(tile.i + 1, bottom + 1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        match: List[Tile] = []

        if len(h_match) >= 2:
            for t in h_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(v_match) >= 2:
            for t in v_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(match) > 0:
            if tile not in self.in_match:
                self.in_match.add(tile)
                match.append(tile)

        for t in match:
            match += self._calculate_match_rec(t)

        self.in_stack.remove(tile)
        return match

    def calculate_matches_for(
        self, new_tiles: List[Tile]
    ) -> Optional[List[List[Tile]]]:
        self.in_match: Set[Tile] = set()
        self.in_stack: Set[Tile] = set()

        for tile in new_tiles:
            if tile in self.in_match:
                continue
            match = self._calculate_match_rec(tile)
            if len(match) > 0:
                self.matches.append(match)

        delattr(self, "in_match")
        delattr(self, "in_stack")

        return self.matches if len(self.matches) > 0 else None

    def remove_matches(self) -> None:
        for match in self.matches:
            for tile in match:
                self.tiles[tile.i][tile.j] = None

        self.matches = []

    def get_falling_tiles(self) -> Tuple[Any, Dict[str, Any]]:
        # List of tweens to create
        tweens: Tuple[Tile, Dict[str, Any]] = []

        # for each column, go up tile by tile until we hit a space
        for j in range(settings.BOARD_WIDTH):
            space = False
            space_i = -1
            i = settings.BOARD_HEIGHT - 1

            while i >= 0:
                tile = self.tiles[i][j]

                # if our previous tile was a space
                if space:
                    # if the current tile is not a space
                    if tile is not None:
                        self.tiles[space_i][j] = tile
                        tile.i = space_i

                        # set its prior position to None
                        self.tiles[i][j] = None

                        tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))
                        space = False
                        i = space_i
                        space_i = -1
                elif tile is None:
                    space = True

                    if space_i == -1:
                        space_i = i

                i -= 1

        # create a replacement tiles at the top of the screen
        for j in range(settings.BOARD_WIDTH):
            for i in range(settings.BOARD_HEIGHT):
                tile = self.tiles[i][j]

                if tile is None:
                    tile = Tile(
                        i,
                        j,
                        random.randint(0, settings.NUM_COLORS - 1),
                        random.randint(0, settings.NUM_VARIETIES - 1),
                    )
                    tile.y -= settings.TILE_SIZE
                    self.tiles[i][j] = tile
                    tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))

        return tweens
