import tcod
import tcod.event
from enum import Enum, auto

from input_handlers import handle_event
from ui import UIPanel
from renderer import Renderer
from action_processor import ActionProcessor
from combat_system import CombatSystem


class GameState(Enum):
    PLAYING = auto()
    SPELL_MENU = auto()
    TARGETING = auto()


class Engine:
    MAP_OFFSET_X = 20  # Agora é uma constante da classe

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

        self.GameState = GameState  # Expor o enum
        self.state = GameState.PLAYING
        self.running = True

        self.target_x = player.x
        self.target_y = player.y

        self.projectiles = []
        self.floating_texts = []

        # Inicializar sistemas
        self.ui_panel = UIPanel(
            x=0,
            width=self.MAP_OFFSET_X,
            height=console.height,
        )
        self.renderer = Renderer(console, self.ui_panel)
        self.action_processor = ActionProcessor(self)
        self.combat_system = CombatSystem(self)

    def run(self):
        while self.running:
            # Renderizar tudo
            self.renderer.render_all(self)

            # Processar eventos
            for event in tcod.event.get():
                self.context.convert_event(event)

                if isinstance(event, tcod.event.Quit):
                    self.running = False
                    return

                action = handle_event(event)
                if action:
                    self.action_processor.process(action)

            # Atualizar projéteis (combate)
            self.combat_system.update_projectiles()