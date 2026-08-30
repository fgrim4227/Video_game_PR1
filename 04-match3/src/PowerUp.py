from src.Tile import Tile
from typing import Callable, List
import settings
import pygame
def line_clear_func(board, tile):
    tiles_to_destroy = []
    for row in range(settings.BOARD_HEIGHT):
        if board.tiles[row][tile.j] is not None:
            tiles_to_destroy.append(board.tiles[row][tile.j])
            
    for col in range(settings.BOARD_WIDTH):
        if board.tiles[tile.i][col] is not None:
            tiles_to_destroy.append(board.tiles[tile.i][col])
            
    return tiles_to_destroy

def color_clear_func(board, tile):
    tiles_to_destroy = []
    for row in board.tiles:
         for t in row:
              if t is not None and t.color == tile.color:
                   tiles_to_destroy.append(t)
    return tiles_to_destroy
        
POWERUP_EFFECTS = {4: line_clear_func, 5: color_clear_func}

class Powerup(Tile):
    def __init__(self, i: int, j: int, color: int, variety: int, size_match: int):
        super().__init__(i, j, color, variety)
        self.size_match = size_match
        self.pw_effect = POWERUP_EFFECTS.get(size_match, None)

    def activate(self, board) -> List[Tile]:
        if self.pw_effect:
            return self.pw_effect(board, self)
        return []
    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:

        self.alpha_surface.blit(
            settings.TEXTURES["tiles"],
            (0, 0),
            settings.FRAMES["tiles"][self.color][self.variety],
        )
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        surface.blit(
            settings.TEXTURES["tiles"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["tiles"][self.color][self.variety],
        )
        frame_idx = 0 if self.size_match == 4 else 1 
        
        surface.blit(
            settings.TEXTURES["power-ups"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["power-ups"][frame_idx]
        )