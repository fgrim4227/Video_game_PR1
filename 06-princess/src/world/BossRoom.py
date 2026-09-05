import settings
from src.world.Room import Room
from src.Boss import Boss
from src.states.entity.EntityIdleState import EntityIdleState
class BossRoom(Room):
    def __init__(self, player, on_game_over):
        # Al llamar al super, forzamos que no genere cofres
        super().__init__(player, on_game_over, generate_chest=False)

    def _generate_entities(self) -> None:
        """Solo genera al Jefe en el centro opuesto a la puerta"""
        boss_x = settings.MAP_RENDER_OFFSET_X + (settings.MAP_WIDTH // 2) * settings.TILE_SIZE
        boss_y = settings.MAP_RENDER_OFFSET_Y + (settings.MAP_HEIGHT // 2) * settings.TILE_SIZE - 32
        
        boss = Boss(
            x=boss_x,
            y=boss_y,
            width=32,  
            height=32,
            walk_speed=0, 
            health=10,
            animation_defs={
                "idle-down": {"frames": [1, 2], "interval": 0.2, "texture": "boss_idle"},
                "idle-up": {"frames": [1, 2], "interval": 0.2, "texture": "boss_idle"},
                "idle-left": {"frames": [1, 2], "interval": 0.2, "texture": "boss_idle"},
                "idle-right": {"frames": [1, 2], "interval": 0.2, "texture": "boss_idle"},
            },
            states={}
        )
        boss.state_machine.states = {
            "idle": lambda sm, e=boss: EntityIdleState(e, sm)
        }
        boss.change_state("idle")
        
        self.entities.append(boss)

    def _generate_objects(self) -> None:
        """La arena del jefe no debe tener vasijas ni interruptores"""
        pass

    def _generate_walls_and_floors(self) -> None:
        super()._generate_walls_and_floors()
        # Aquí cerramos todas las puertas directamente para crear la "arena"
        for doorway in self.doorways:
            doorway.open = False