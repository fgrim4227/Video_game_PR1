"""
ISPPV1 2023
Study Case: Pong

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the main program to run the pong game.
"""
import pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
from src.Pong import Pong

if __name__ == "__main__":
    game = Pong()
    game.exec()
