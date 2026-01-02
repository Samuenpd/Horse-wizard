import tcod
import tcod.event
from enum import Enum, auto

import ai
from input_handlers import handle_event
from ui import UIPanel


MAP_OFFSET_X = 20

class GameState(Enum):
    PLAYING = auto()
    SPELL_MENU = auto()
    TARGETING = auto()


class Engine:
    def __init__(
        self,
        *,
        entities,
        game_map,
        player,
        context,
        console,
    ):
        self.entities = entities
        self.game_map = game_map
        self.player = player
        self.context = context
        self.console = console

        self.state = GameState.PLAYING
        self.running = True

        self.target_x = player.x
        self.target_y = player.y

        self.projectiles = []

        self.ui_panel = UIPanel(
            x=0,
            width=MAP_OFFSET_X,
            height=console.height,
        )

    # ================= MAIN LOOP =================

    def run(self):
        while self.running:
            self.render()

            for event in tcod.event.get():
                self.context.convert_event(event)

                if isinstance(event, tcod.event.Quit):
                    self.running = False
                    return

                action = handle_event(event)
                if action:
                    self.process_action(action)

            # ===== UPDATE DOS PROJÉTEIS =====
            for projectile in self.projectiles[:]:
                projectile.update()

                px, py = projectile.x, projectile.y
                hit_entity = None

                for entity in self.entities:
                    if entity is self.player:
                        continue

                    if entity.x == px and entity.y == py and hasattr(entity, "fighter"):
                        entity.fighter.take_damage(projectile.damage)

                        if entity.fighter.hp <= 0:
                            hit_entity = entity

                        break  # projétil para no primeiro alvo

                if hit_entity:
                    self.entities.remove(hit_entity)

                if hit_entity or projectile.finished():
                    self.projectiles.remove(projectile)

    # ================= ACTIONS =================

    def process_action(self, action):
        match action["type"]:
            case "move":
                self.player.move(
                    action["dx"],
                    action["dy"],
                    self.game_map,
                    self.entities,
                )

                # ===== TURNO DOS INIMIGOS =====
                for entity in self.entities:
                    if entity is self.player:
                        continue

                    if not hasattr(entity, "fighter"):
                        continue

                    # delay opcional
                    if hasattr(entity, "turn_delay"):
                        entity.turn_counter += 1
                        if entity.turn_counter < entity.turn_delay:
                            continue
                        entity.turn_counter = 0

                        ai.move_towards(
                            entity,
                            self.player.x,
                            self.player.y,
                            self.game_map,
                            self.entities,
                        )

                # remove mortos restantes
                for entity in self.entities[:]:
                    if hasattr(entity, "fighter") and entity.fighter.hp <= 0:
                        self.entities.remove(entity)

            case "select_spell":
                spell = self.player.spellbook.select(action["spell_id"])
                if spell and spell.requires_target:
                    self.state = GameState.TARGETING
                else:
                    self.state = GameState.PLAYING  
                    
            case "confirm_target":
                if self.state != GameState.TARGETING:
                    return

                self.player.spellbook.cast_active(
                    self,
                    int(self.target_x),
                    int(self.target_y),
                )
                self.state = GameState.PLAYING

            case "cancel":
                self.player.spellbook.active_spell = None
                self.state = GameState.PLAYING

            case "mouse_move":
                if self.state == GameState.TARGETING:
                    map_x = action["x"] - MAP_OFFSET_X
                    map_y = action["y"]

                    if self.game_map.in_bounds(map_x, map_y):
                        self.target_x = map_x
                        self.target_y = map_y


            case "quit":
                self.running = False

    # ================= RENDER =================

    def render(self):
        self.console.clear()

        # ===== UI PANEL =====
        self.ui_panel.render(
            self.console,
            self.player,
            self.state,
        )

        # ===== MAPA =====
        self.game_map.render(self.console, offset_x=MAP_OFFSET_X)

        # ===== ENTIDADES =====
        for entity in self.entities:
            self.console.print(
                entity.x + MAP_OFFSET_X,
                entity.y,
                entity.glyph,
                fg=entity.color,
            )

        # ===== PROJÉTEIS =====
        for projectile in self.projectiles:
            if projectile.x is None or projectile.y is None:
                continue

            self.console.print(
                projectile.x + MAP_OFFSET_X,
                projectile.y,
                projectile.glyph,
                fg=projectile.color,
            )

        # ===== TARGETING =====
        if self.state == GameState.TARGETING:
            self.console.print(
                int(self.target_x) + MAP_OFFSET_X,
                int(self.target_y),
                "X",
                fg=(255, 0, 0),
            )

        self.context.present(self.console)

