
import pygame

from gale.factory import Factory
from src.Strategy import Strategy
from src.LogPair import LogPair
import settings
import random

class EasyMode(Strategy):
    def __init__(self):
        self.log_pair_factory : Factory = Factory(LogPair)
    def generation(self, world, dt, score):
        if world.generate_logs:
            world.logs_spawn_timer += dt
            #Aca tendriamos que pasarle logica al strategy
            if world.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
                world.logs_spawn_timer = 0.0
                y = max(
                    -settings.LOG_HEIGHT + 10,
                    min(
                        world.last_log_y + random.randint(-20, 20),
                        settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                    ),
                )
                world.last_log_y = y
                world.logs.append(self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y))
    def handle_input(self, input_id, input_data, bird):
        #Nada
        pass