"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Room.
"""

import random
from typing import Any, Callable, List, Optional, TypeVar

import pygame

from gale.tilemap import TileMap

import settings
from src.definitions.entity import ENTITY_DEFS
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Entity import Entity
from src.GameObject import GameObject
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.world.Doorway import Doorway

_ENEMY_TYPES = ["skeleton", "slime", "bat", "ghost", "spider"]

# Door archway detection zones, in the same room-local coordinates as
# every entity's x/y (not screen space, so this works regardless of
# camera/adjacent-room render offsets). Wider than the doorway's own
# get_collision_rect() on purpose -- these only decide *whether* the
# player is close enough to a doorway to bother clipping at all; the
# actual visible shape while crossing is the doorway's own, narrower,
# rect (see _doorway_opening_for below), applied with gale.stencil in
# Entity.render_sprite so the player is seen passing through the wall
# opening -- clipped by its edges -- instead of popping in and out of
# existence.
_DOORWAY_ZONES = {
    "left": pygame.Rect(
        -settings.TILE_SIZE - 6,
        settings.MAP_RENDER_OFFSET_Y + settings.MAP_HEIGHT // 2 * settings.TILE_SIZE - settings.TILE_SIZE * 2,
        settings.TILE_SIZE * 2 + 6,
        settings.TILE_SIZE * 3,
    ),
    "right": pygame.Rect(
        settings.MAP_RENDER_OFFSET_X + settings.MAP_WIDTH * settings.TILE_SIZE - 6,
        settings.MAP_RENDER_OFFSET_Y + settings.MAP_HEIGHT // 2 * settings.TILE_SIZE - settings.TILE_SIZE * 2,
        settings.TILE_SIZE * 2 + 6,
        settings.TILE_SIZE * 3,
    ),
    "top": pygame.Rect(
        settings.MAP_RENDER_OFFSET_X + settings.MAP_WIDTH // 2 * settings.TILE_SIZE - settings.TILE_SIZE,
        -settings.TILE_SIZE - 6,
        settings.TILE_SIZE * 2,
        settings.TILE_SIZE * 2 + 12,
    ),
    "bottom": pygame.Rect(
        settings.MAP_RENDER_OFFSET_X + settings.MAP_WIDTH // 2 * settings.TILE_SIZE - settings.TILE_SIZE,
        settings.VIRTUAL_HEIGHT - settings.TILE_SIZE - 6,
        settings.TILE_SIZE * 2,
        settings.TILE_SIZE * 2 + 12,
    ),
}


def _doorway_opening_for(
    rect: pygame.Rect, doorways_by_direction: dict
) -> Optional[pygame.Rect]:
    """
    :returns: The precise opening rect of whichever doorway rect is
        close to (i.e. overlapping the wider detection zone of), or
        None if rect isn't near any doorway right now.
    """
    for direction, zone in _DOORWAY_ZONES.items():
        if zone.colliderect(rect):
            return doorways_by_direction[direction].get_collision_rect()

    return None


class Room:
    def __init__(
        self,
        player: TypeVar("Player"),
        on_game_over: Callable[[], None],
        generate_chest: bool = False
    ) -> None:
        # Reference to player for collisions, etc.
        self.player = player
        self.on_game_over = on_game_over
        self.generate_chest = generate_chest
        self.width = settings.MAP_WIDTH
        self.height = settings.MAP_HEIGHT
                # Doorways that lead to other dungeon rooms.
        self.doorways = [
            Doorway("top", False, self),
            Doorway("bottom", False, self),
            Doorway("left", False, self),
            Doorway("right", False, self),
        ]
        self._doorways_by_direction = {
            doorway.direction: doorway for doorway in self.doorways
        }
        self.tilemap = TileMap(settings.TILE_SIZE, settings.TILE_SIZE, self.width, self.height)
        self.tilemap.add_tileset(settings.TILESET)
        self._generate_walls_and_floors()

        self.entities: List[Entity] = []
        self._generate_entities()

        self.objects: List[GameObject] = []
        self._generate_objects()

        # Used for centering the dungeon rendering.
        self.render_offset_x = settings.MAP_RENDER_OFFSET_X
        self.render_offset_y = settings.MAP_RENDER_OFFSET_Y

        # Used for drawing when this room is the next room, adjacent to the
        # active one, while sliding between rooms.
        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        self.projectiles: List[Any] = []

    def update(self, dt: float) -> None:
        # Don't update anything if we are sliding to another room.
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt)

        for entity in self.entities:
            if entity.health <= 0:
                entity.dead = True

                # Chance to drop a heart.
                if not entity.dropped and random.randint(1, 10) == 1:
                    self.objects.append(
                        GameObject(GAME_OBJECT_DEFS["heart"], entity.x, entity.y)
                    )

                # Whether the entity dropped or not, it is assumed that it did.
                entity.dropped = True
            elif not entity.dead:
                entity.process_ai(self, dt)
                entity.update(dt)

            # Collision between the player and entities in the room.
            if (
                not entity.dead
                and self.player.collides(entity)
                and not self.player.invulnerable
            ):
                settings.SOUNDS["hit-player"].play()
                self.player.damage(1)
                self.player.go_invulnerable(1.5)

                if self.player.health == 0:
                    self.on_game_over()

        self.entities = [entity for entity in self.entities if not entity.dead]

        for obj in list(self.objects):
            obj.update(dt)

            if self.player.collides(obj):
                obj.on_collide()

                if obj.solid and not obj.taken:
                    self._push_player_out_of(obj)

                if obj.consumable:
                    obj.on_consume(self.player, obj)
                    self.objects.remove(obj)


        for projectile in list(self.projectiles):
            projectile.update(dt)

            for entity in self.entities:
                if projectile.dead:
                    break

                if not entity.dead and projectile.collides(entity):
                    entity.damage(1)
                    settings.SOUNDS["hit-enemy"].play()
                    projectile.dead = True

            if projectile.dead:
                self.projectiles.remove(projectile)

    def _push_player_out_of(self, obj: GameObject) -> None:
        player = self.player
        player_y = player.y + player.height / 2
        player_height = player.height - player.height / 2
        player_right = player.x + player.width
        player_bottom = player_y + player_height

        if (
            player.direction == "left"
            and not (player_y >= (obj.y + obj.height))
            and not (player_bottom <= obj.y)
        ):
            player.x = obj.x + obj.width
        elif (
            player.direction == "right"
            and not (player_y >= (obj.y + obj.height))
            and not (player_bottom <= obj.y)
        ):
            player.x = obj.x - player.width
        elif (
            player.direction == "down"
            and not (player.x >= (obj.x + obj.width))
            and not (player_right <= obj.x)
        ):
            player.y = obj.y - player.height
        elif (
            player.direction == "up"
            and not (player.x >= (obj.x + obj.width))
            and not (player_right <= obj.x)
        ):
            player.y = obj.y + obj.height - player.height / 2

    def interact_adjacent(self, player: TypeVar("Player")) -> None:
        """
        Looks for a takeable object directly in front of the player (one
        tile away, in the direction they're currently facing) and, if
        found, removes it from the room and has the player lift it.
        """
        player_y = player.y + player.height / 2
        player_height = player.height - player.height / 2
        player_col = int((player.x + player.width / 2) // settings.TILE_SIZE)
        player_row = int((player_y + player_height / 2) // settings.TILE_SIZE)

        for obj in self.objects:
            if not obj.takeable and not getattr(obj, 'interactable', False):
                continue

            obj_col = int((obj.x + obj.width / 2) // settings.TILE_SIZE)
            obj_row = int((obj.y + obj.height / 2) // settings.TILE_SIZE)

            adjacent = (
                (player.direction == "right" and obj_row == player_row and obj_col == player_col + 1)
                or (player.direction == "left" and obj_row == player_row and obj_col == player_col - 1)
                or (player.direction == "up" and obj_col == player_col and obj_row == player_row - 1)
                or (player.direction == "down" and obj_col == player_col and obj_row == player_row + 1)
            )

            if adjacent:
                if obj.takeable:
                    self.objects.remove(obj)
                    player.change_state("pot-lift", pot=obj)
                elif obj.interactable:
                    obj.on_interact(player, obj)
                    return

    def _generate_walls_and_floors(self) -> None:
        """
        Generates the walls and floors of the room, randomizing the various
        varieties of said tiles for visual variety.
        """
        floor = self.tilemap.add_layer("floor")

        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                if x == 1 and y == 1:
                    tile_id = settings.TILE_TOP_LEFT_CORNER
                elif x == 1 and y == self.height:
                    tile_id = settings.TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    tile_id = settings.TILE_TOP_RIGHT_CORNER
                elif x == self.width and y == self.height:
                    tile_id = settings.TILE_BOTTOM_RIGHT_CORNER
                elif x == 1:
                    tile_id = random.choice(settings.TILE_LEFT_WALLS)
                elif x == self.width:
                    tile_id = random.choice(settings.TILE_RIGHT_WALLS)
                elif y == 1:
                    tile_id = random.choice(settings.TILE_TOP_WALLS)
                elif y == self.height:
                    tile_id = random.choice(settings.TILE_BOTTOM_WALLS)
                else:
                    tile_id = random.choice(settings.TILE_FLOORS)

                floor[y - 1][x - 1] = tile_id

    def _generate_entities(self) -> None:
        """Randomly creates an assortment of enemies for the player to fight."""
        for _ in range(10):
            enemy_type = random.choice(_ENEMY_TYPES)
            definition = ENTITY_DEFS[enemy_type]

            entity = Entity(
                x=random.randint(
                    settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE,
                    settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2 - 16,
                ),
                y=random.randint(
                    settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE,
                    settings.MAP_HEIGHT * settings.TILE_SIZE
                    + settings.MAP_RENDER_OFFSET_Y
                    - settings.TILE_SIZE
                    - 16,
                ),
                width=16,
                height=16,
                walk_speed=definition.get("walk_speed", 20),
                health=1,
                animation_defs=definition["animations"],
                states={},
            )

            entity.state_machine.states = {
                "walk": lambda sm, e=entity: EntityWalkState(e, sm),
                "idle": lambda sm, e=entity: EntityIdleState(e, sm),
            }
            entity.change_state("walk")
            self.entities.append(entity)

    def _generate_objects(self) -> None:
        """Genera los obstáculos, el interruptor y el cofre si corresponde."""

        switch = GameObject(
            GAME_OBJECT_DEFS["switch"],
            random.randint(
                settings.MAP_RENDER_OFFSET_X + settings.TILE_SIZE,
                settings.VIRTUAL_WIDTH - settings.TILE_SIZE * 2 - 16,
            ),
            random.randint(
                settings.MAP_RENDER_OFFSET_Y + settings.TILE_SIZE,
                settings.VIRTUAL_HEIGHT - settings.TILE_SIZE * 2 - 16,
            ),
        )
        self.objects.append(switch)

        def open_all_doors() -> None:
            if switch.state == "unpressed":
                switch.state = "pressed"
                for doorway in self.doorways:
                    doorway.open = True
                settings.SOUNDS["door"].play()

        switch.on_collide = open_all_doors

        if self.generate_chest:
            chest_x = settings.MAP_RENDER_OFFSET_X + (settings.MAP_WIDTH // 2) * settings.TILE_SIZE
            chest_y = settings.MAP_RENDER_OFFSET_Y + (settings.MAP_HEIGHT // 2) * settings.TILE_SIZE
            chest = GameObject(GAME_OBJECT_DEFS["chest"], chest_x, chest_y)
            self.objects.append(chest)

            for doorway in self.doorways:
                doorway.open = False

        for y in range(2, self.height):
            for x in range(2, self.width):
                if self.generate_chest:
                    if abs(x - self.width // 2) <= 1 and abs(y - self.height // 2) <= 1:
                        continue
                
                if random.randint(1, 20) == 1:
                    self.objects.append(
                        GameObject(GAME_OBJECT_DEFS["pot"], x * 16, y * 16)
                    )
    def render(
        self,
        surface: pygame.Surface,
        camera_offset_x: float = 0,
        camera_offset_y: float = 0,
    ) -> None:
        offset_x = self.adjacent_offset_x + camera_offset_x
        offset_y = self.adjacent_offset_y + camera_offset_y

        # Not tilemap.render(surface): offset_x/offset_y can carry the room
        # a full VIRTUAL_WIDTH/HEIGHT off-screen mid room-shift, and
        # Surface.subsurface() (used for 07-ultimate_fantasy's BattleState,
        # whose offset is fixed and always in-bounds) requires the rect to
        # land fully inside surface -- a plain blit per tile, sourcing the
        # gid/rect from the TileMap/Tileset instead of the old self.tiles
        # list and settings.frame("tiles", ...), has no such restriction.
        for y in range(self.height):
            for x in range(self.width):
                gid = self.tilemap.get_gid("floor", y, x)
                tileset = self.tilemap.tileset_for_gid(gid)
                surface.blit(
                    tileset.image,
                    (
                        x * settings.TILE_SIZE + self.render_offset_x + offset_x,
                        y * settings.TILE_SIZE + self.render_offset_y + offset_y,
                    ),
                    tileset.rect_for(gid),
                )

        for doorway in self.doorways:
            doorway.render(surface, offset_x, offset_y)

        for obj in self.objects:
            obj.render(surface, offset_x, offset_y)

        for entity in self.entities:
            if not entity.dead:
                entity.render(surface, offset_x, offset_y)

        # The player and projectiles are drawn using only the camera pan —
        # never this room's own adjacent_offset — matching the original,
        # where Player:render()/Projectile:render() take no room offset at
        # all. Their x/y already track the correct absolute (pre-camera-pan)
        # screen position on their own, including mid-tween during a room
        # shift; adding adjacent_offset on top (as tiles/entities do) would
        # draw them a full room-width off from where they actually are.
        #
        # While the player is near a doorway, clip their sprite to that
        # doorway's own opening rect (via gale.stencil, applied inside
        # Entity.render_sprite) instead of hiding them outright: the part
        # of the sprite still overlapping solid wall disappears, but the
        # part inside the opening keeps showing, so walking (or, mid
        # room-shift, tweening) through the gap reads as passing under/
        # through the archway rather than blinking out of existence.
        if self.player:
            self.player.visibility_clip_rect = _doorway_opening_for(
                self.player.get_collision_rect(), self._doorways_by_direction
            )
            self.player.render(surface, camera_offset_x, camera_offset_y)
            self.player.visibility_clip_rect = None

        for projectile in self.projectiles:
            if not _doorway_opening_for(
                projectile.get_collision_rect(), self._doorways_by_direction
            ):
                projectile.render(surface, camera_offset_x, camera_offset_y)
