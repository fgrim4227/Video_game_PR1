from src.Projectile import Projectile
from src.GameObject import GameObject
from src.definitions.game_objects import GAME_OBJECT_DEFS

class ArrowFactory:
    @staticmethod
    def create(entity) -> Projectile:
        # 1. Creamos la flecha real usando la definición
        arrow_obj = GameObject(
            GAME_OBJECT_DEFS["arrow"], 
            entity.x, 
            entity.y
        )
        
        # 2. Convertimos ese objeto en un proyectil y lo disparamos
        return Projectile(arrow_obj, entity.direction)