
import pygame
import random
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from src.LogPair import LogPair 
import settings

class Strategy():
    def __init__(self):
        pass
    def generation(self, world, dt, score):
        #Logica de generacion de troncos
        pass
    def handle_input(self, input_id : str, input_data : InputData, bird):
        pass