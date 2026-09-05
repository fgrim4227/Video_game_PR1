"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the game settings that include the association of the
inputs with an their ids, constants of values to set up the game, sounds,
textures, frames, and fonts.
"""

import pathlib

import pygame

from gale import frames
from gale import input_handler
from gale import tilemap

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_ESCAPE, "quit")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_LEFT, "move_left")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RIGHT, "move_right")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_UP, "move_up")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_DOWN, "move_down")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SPACE, "sword")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_RETURN, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_KP_ENTER, "enter")
input_handler.InputHandler.set_keyboard_action(input_handler.KEY_x, "bow")
TITLE = "The Legend of the Princess"

BASE_DIR = pathlib.Path(__file__).parent

VIRTUAL_WIDTH = 384
VIRTUAL_HEIGHT = 216

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

TILE_SIZE = 16

#
# map constants
#
MAP_WIDTH = VIRTUAL_WIDTH // TILE_SIZE - 2
MAP_HEIGHT = VIRTUAL_HEIGHT // TILE_SIZE - 2

MAP_RENDER_OFFSET_X = (VIRTUAL_WIDTH - MAP_WIDTH * TILE_SIZE) // 2
MAP_RENDER_OFFSET_Y = (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) // 2

#
# tile IDs (1-based, matching the tilesheet's row-major slicing)
#
TILE_TOP_LEFT_CORNER = 4
TILE_TOP_RIGHT_CORNER = 5
TILE_BOTTOM_LEFT_CORNER = 23
TILE_BOTTOM_RIGHT_CORNER = 24

TILE_EMPTY = 19

TILE_FLOORS = [
    7, 8, 9, 10, 11, 12, 13,
    26, 27, 28, 29, 30, 31, 32,
    45, 46, 47, 48, 49, 50, 51,
    64, 65, 66, 67, 68, 69, 70,
    88, 89, 107, 108,
]

TILE_TOP_WALLS = [58, 59, 60]
TILE_BOTTOM_WALLS = [79, 80, 81]
TILE_LEFT_WALLS = [77, 96, 115]
TILE_RIGHT_WALLS = [78, 97, 116]

TEXTURES = {
    "tiles": pygame.image.load(BASE_DIR / "assets" / "graphics" / "tilesheet.png"),
    "background": pygame.image.load(BASE_DIR / "assets" / "graphics" / "background.png"),
    "character-walk": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "character_walk.png"
    ),
    "character-swing-sword": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "character_swing_sword.png"
    ),
    "hearts": pygame.image.load(BASE_DIR / "assets" / "graphics" / "hearts.png"),
    "switches": pygame.image.load(BASE_DIR / "assets" / "graphics" / "switches.png"),
    "entities": pygame.image.load(BASE_DIR / "assets" / "graphics" / "entities.png"),
    "character-pot-lift": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "character_pot_lift.png"
    ),
    "character-pot-walk": pygame.image.load(
        BASE_DIR / "assets" / "graphics" / "character_pot_walk.png"
    ),
    "boss_idle": pygame.image.load(BASE_DIR / "assets" / "graphics" / "boss_idle.png"),
    "character-bow": pygame.image.load(BASE_DIR / "assets" / "graphics" / "character_bow.png"),
    "chests": pygame.image.load(BASE_DIR / "assets" / "graphics" / "chests.png"),
    "fireball": pygame.image.load(BASE_DIR / "assets" / "graphics" / "fireball.png"),
    "arrow": pygame.image.load(BASE_DIR / "assets" / "graphics" / "arrow.png"),
}

# Used by Room's gale.tilemap.TileMap: TILE_* ids above are 1-based,
# matching this tileset's default first_gid, so they double as gids.
TILESET = tilemap.Tileset(TEXTURES["tiles"], TILE_SIZE, TILE_SIZE)

FRAMES = {
    "tiles": frames.generate_frames(TEXTURES["tiles"], 16, 16),
    "character-walk": frames.generate_frames(TEXTURES["character-walk"], 16, 32),
    "character-swing-sword": frames.generate_frames(
        TEXTURES["character-swing-sword"], 32, 32
    ),
    "hearts": frames.generate_frames(TEXTURES["hearts"], 16, 16),
    "switches": frames.generate_frames(TEXTURES["switches"], 16, 18),
    "entities": frames.generate_frames(TEXTURES["entities"], 16, 16),
    "character-pot-lift": frames.generate_frames(TEXTURES["character-pot-lift"], 16, 32),
    "character-pot-walk": frames.generate_frames(TEXTURES["character-pot-walk"], 16, 32),
    "boss_idle": frames.generate_frames(TEXTURES["boss_idle"], 32, 32),

    "character-bow": frames.generate_frames(TEXTURES["character-bow"], 16, 32),
    "chests": frames.generate_frames(TEXTURES["chests"], 16, 16),
    "fireball": frames.generate_frames(TEXTURES["fireball"], 16, 16),
    "arrow": frames.generate_frames(TEXTURES["arrow"], 15, 4),
}


def frame(texture_id, one_based_index):
    """
    Every frame index in this project's own code (tile IDs, quad numbers,
    animation frame lists) is written 1-based, matching the original
    Lua/LOVE2D source it was ported from, since gale.frames.generate_frames
    (like Lua tables) still needs a 0-based lookup.
    """
    return FRAMES[texture_id][one_based_index - 1]


FONTS = {
    "princess": pygame.font.Font(BASE_DIR / "assets" / "fonts" / "princess.otf", 32),
    "princess-small": pygame.font.Font(
        BASE_DIR / "assets" / "fonts" / "princess.otf", 24
    ),
}

SOUNDS = {
    "sword": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "sword.wav"),
    "hit-enemy": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "hit_enemy.wav"),
    "hit-player": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "hit_player.wav"),
    "door": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "door.wav"),
    "heart-taken": pygame.mixer.Sound(
        BASE_DIR / "assets" / "sounds" / "heart_taken.wav"
    ),
    "pot-wall": pygame.mixer.Sound(BASE_DIR / "assets" / "sounds" / "pot_wall.wav"),
}

MUSIC = {
    "start": str(BASE_DIR / "assets" / "sounds" / "start_music.mp3"),
    "dungeon": str(BASE_DIR / "assets" / "sounds" / "dungeon_music.mp3"),
    "game-over": str(BASE_DIR / "assets" / "sounds" / "game_over_music.mp3"),
}

COLOR_TITLE_SHADOW = (34, 34, 34)
COLOR_TITLE = (175, 53, 42)
COLOR_WHITE = (255, 255, 255)
