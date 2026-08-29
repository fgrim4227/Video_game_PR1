"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains a function to fetch and store the tile frames.
"""

from typing import List

import pygame

from gale.frames import generate_frames

import settings


def generate_tile_frames(spritesheet: pygame.Surface) -> List[List[pygame.Rect]]:
    """
    match3.png is a plain settings.TILE_SIZE grid (gale.frames.generate_frames
    slices it), but two "colors" (each with settings.NUM_VARIETIES tiles) sit
    side by side in every row of the sheet, so each row is split into its
    two color groups on top of that.
    """
    flat_frames = generate_frames(spritesheet, settings.TILE_SIZE, settings.TILE_SIZE)
    cols_per_row = spritesheet.get_width() // settings.TILE_SIZE

    frames = []

    for row_start in range(0, len(flat_frames), cols_per_row):
        row = flat_frames[row_start : row_start + cols_per_row]

        for color_start in range(0, len(row), settings.NUM_VARIETIES):
            frames.append(row[color_start : color_start + settings.NUM_VARIETIES])

    return frames
