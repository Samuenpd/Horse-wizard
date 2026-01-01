import tcod.event
from game_state import GameState
from enum import Enum

class GameState(Enum):
    PLAYING = 1
    SPELL_MENU = 2
    TARGETING = 3


class Engine:
    def __init__(self, entities, game_map, context, console, spell_library):
        self.entities = entities
        self.player = entities[0]
        self.game_map = game_map
        self.context = context
        self.console = console
        self.spell_library = spell_library

        self.state = GameState.PLAYING

        # dados da mira
        self.target_x = 0
        self.target_y = 0
        self.target_spell = None

    # === MÉTODO ISOLADO DA MIRA ===
    def start_targeting(self, spell_name: str):
        self.state = GameState.TARGETING
        self.target_spell = spell_name
        self.target_x = self.player.x
        self.target_y = self.player.y

    def finish_targeting(self):
        from actions import CastSpellAction

        action = CastSpellAction(
            self.player,
            self.target_spell,
            self.target_x,
            self.target_y
        )

        self.state = GameState.PLAYING
        self.target_spell = None

        self.process_action(action)

    def cancel_targeting(self):
        self.state = GameState.PLAYING
        self.target_spell = None

    def process_action(self, action):
        if action:
            action.perform(self)

    def toggle_spell_menu(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.SPELL_MENU
        else:
            self.state = GameState.PLAYING

    def handle_input(self):
        for event in tcod.event.wait():
            action = handle_event(event)

            if action and self.state == GameState.PLAYER_TURN:
                self.process_player_action(action)

            if action and action.get("exit"):
                self.running = False

    def process_player_action(self, action):
        dx = action.get("dx", 0)
        dy = action.get("dy", 0)

        if dx or dy:
            self.player.move(dx, dy, self.game_map)
            self.state = GameState.ENEMY_TURN

    def enemy_turn(self):
        for entity in self.entities:
            if entity is not self.player and hasattr(entity, "ai"):
                entity.ai.take_turn(self.player, self.game_map)

        self.state = GameState.PLAYER_TURN

    def update(self):
        if self.state == GameState.ENEMY_TURN:
            self.enemy_turn()

    def render(self):
        self.console.clear()

        self.game_map.render(self.console)

        for entity in self.entities:
            entity.draw(self.console)

        if self.state == GameState.TARGETING:
            self.console.print(
                self.target_x,
                self.target_y,
                "X",
                fg=(255, 0, 0)
            )

    def render_spell_menu(self):
        x = 2
        y = 2

        self.console.print(x, y, "=== SPELLS ===", fg=(255, 255, 0))
        y += 2

        for spell in self.player.spellbook.known_spells:
            self.console.print(x, y, f"- {spell}")
            y += 1

        y += 1
        self.console.print(x, y, "Slots:")
        y += 1

        for slot, spell in self.player.spellbook.slots.items():
            self.console.print(x, y, f"{slot}: {spell}")
            y += 1

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()
