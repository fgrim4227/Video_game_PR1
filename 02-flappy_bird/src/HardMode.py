from gale.factory import Factory
from src.Strategy import Strategy
from src.LogPair import LogPair
from src.CrushLogPair import CrushLogPair
from src.PowerUp import PowerUp
from src.GhostPw import GhostPw
import settings
import random

class HardMode(Strategy):
    def __init__(self):
        self.log_pair_factory: Factory = Factory(LogPair)
        self.crushing_lp_factory: Factory = Factory(CrushLogPair)
        self.ghost_factory: Factory = Factory(GhostPw)
    def generation(self, world, dt, score):
        if world.generate_logs:
            world.logs_spawn_timer += dt
            if world.logs_spawn_timer >= world.current_limit:
                world.logs_spawn_timer = 0.0
                
                # 1. Definir el nuevo límite de tiempo aleatorio para el PRÓXIMO tronco
                world.current_limit = random.uniform(1.35, 1.8)
                
                # 2. Calcular la variación vertical permitida (pendiente máxima)
                # Escalas la variación usando el tiempo para evitar huecos imposibles
                max_dy = 80 * world.current_limit 
                vertical_pair_gap = random.randint(90, 120)
                bottom_lim = settings.VIRTUAL_HEIGHT - vertical_pair_gap - settings.LOG_HEIGHT - settings.GROUND_HEIGHT - 20
                y = max(
                    -settings.LOG_HEIGHT + 10,
                    min(
                        world.last_log_y + random.randint(int(-max_dy), int(max_dy)),
                        bottom_lim
                    )
                )
                world.last_log_y = y
                
                # 3. Probabilidad escalonada (10% base + 1% cada 10 puntos)
                probabilidad = 10 + (score // 10)
                if random.randint(1, 100) <= probabilidad:
                    world.logs.append(self.crushing_lp_factory.create(settings.VIRTUAL_WIDTH, y, {"log_gap": vertical_pair_gap}))
                else:
                    world.logs.append(self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, {"log_gap": vertical_pair_gap}))
                if random.randint(1, 100) <= 15:
                    pw_y = y + settings.LOG_HEIGHT + (vertical_pair_gap / 2) # Aparece en el medio del gap
                    world.pw_up.append(self.ghost_factory.create(settings.VIRTUAL_WIDTH + 30, pw_y))  
    def handle_input(self, input_id, input_data, bird):
        # Aquí irá el movimiento horizontal
        if(input_id == "left"):
            if (input_data.pressed):
                bird.vx = -settings.BIRD_H_SPEED
            elif(bird.vx < 0 and input_data.released):
                bird.vx = 0
        if(input_id == "right"):
            if(input_data.pressed):
                bird.vx = settings.BIRD_H_SPEED
            elif(bird.vx > 0 and input_data.released):
                bird.vx = 0