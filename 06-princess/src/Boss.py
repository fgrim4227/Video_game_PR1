from src.Entity import Entity
from src.TargetProjectile import TargetProjectile
import random

class Boss(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invulnerable_to_sword = True
        self.vulnerability_timer = 0
        self.fire_timer = 0
        self.health = 10 # Puntos de vida del jefe

    def update(self, dt: float) -> None:
        super().update(dt)
        
        # Gestionar vulnerabilidad
        if not self.invulnerable_to_sword:
            self.vulnerability_timer -= dt
            if self.vulnerability_timer <= 0:
                self.invulnerable_to_sword = True
                self.invulnerable = False # Resetea alpha

    def process_ai(self, room, dt: float) -> None:
        # Lógica de disparo periódico (puedes meter esto en un BossAttackState)
        self.fire_timer -= dt
        if self.fire_timer <= 0:
            self.fire_timer = random.uniform(2.0, 4.0) # Dispara cada 2-4 segundos
            fireball = TargetProjectile(self.x, self.y, room.player.x, room.player.y)
            room.projectiles.append(fireball)
            
    def on_arrow_hit(self):
        # Pierde su inmunidad
        self.invulnerable_to_sword = False
        self.vulnerability_timer = 3.0 # Segundos de vulnerabilidad
        self.invulnerable = True # Dispara el flash_timer de Entity.py para efecto visual