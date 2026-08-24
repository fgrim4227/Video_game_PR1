"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the main program to run the game.
"""

from src.FlappyBird import FlappyBird
import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)

if __name__ == "__main__":
    game = FlappyBird()
    game.exec()
