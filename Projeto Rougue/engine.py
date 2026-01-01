import tcod
import tcod.event
from enum import Enum, auto
from input_handlers import handle_event


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

            # Update projectiles
            for projectile in self.projectiles[:]:
                projectile.update()
                if projectile.finished():
                    self.projectiles.remove(projectile)

    # ================= ACTIONS =================

    def process_action(self, action):
        match action["type"]:
            case "move":
                self.player.move(
                    action["dx"],
                    action["dy"],
                    self.game_map,
                )

            case "open_spell_menu":
                if self.state == GameState.PLAYING:
                    self.state = GameState.SPELL_MENU

            case "select_spell":
                if self.state != GameState.SPELL_MENU:
                    return  # ignora se não estiver no menu

                spell = self.player.spellbook.select(action["spell_id"])
                if spell and spell.requires_target:
                    self.state = GameState.TARGETING
                    self.target_x = self.player.x
                    self.target_y = self.player.y
                elif spell:
                    self.player.spellbook.cast_active(self)
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
                    self.target_x = action["x"]
                    self.target_y = action["y"]

            case "quit":
                self.running = False

    # ================= RENDER =================

    def render(self):
        self.console.clear()
        self.game_map.render(self.console)

        for entity in self.entities:
            self.console.print(
                entity.x,
                entity.y,
                entity.glyph,
                fg=entity.color,
            )

        # Render projectiles
        for projectile in self.projectiles:
            if projectile.x is None or projectile.y is None:
                continue

            self.console.print(
                projectile.x,
                projectile.y,
                projectile.glyph,
                fg=projectile.color,
            )

        if self.state == GameState.TARGETING:
            if self.target_x is not None and self.target_y is not None:
                self.console.print(
                    int(self.target_x),
                    int(self.target_y),
                    "X",
                    fg=(255, 0, 0),
                )

        if self.state == GameState.SPELL_MENU:
            self.render_spell_menu()

        self.context.present(self.console)

    def render_spell_menu(self):
        x, y = 2, 2

        for i, spell in enumerate(self.player.spellbook.known.values()):
            self.console.print(
                x,
                y + i,
                f"{i + 1} - {spell.name} ({spell.cost})",
            )
