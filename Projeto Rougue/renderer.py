import tcod
from ui import UIPanel

MAP_OFFSET_X = 20


class Renderer:
    def __init__(self, console, ui_panel):
        self.console = console
        self.ui_panel = ui_panel

    def render_all(self, engine):
        self.console.clear()

        # UI Panel
        self.ui_panel.render(
            self.console,
            engine.player,
            engine,
        )

        # Mapa
        engine.game_map.render(self.console, offset_x=MAP_OFFSET_X)

        # Entidades
        for entity in engine.entities:
            self.console.print(
                entity.x + MAP_OFFSET_X,
                entity.y,
                entity.glyph,
                fg=entity.color,
            )

        # Textos flutuantes
        for ft in engine.floating_texts[:]:
            if ft.is_alive():
                ft.update()
                self.console.print(
                    int(ft.x) + MAP_OFFSET_X,
                    int(ft.y),
                    ft.text,
                    fg=ft.color,
                )

        # Remover textos mortos
        engine.floating_texts = [ft for ft in engine.floating_texts if ft.is_alive()]

        # Projéteis
        for projectile in engine.projectiles:
            if projectile.x is None or projectile.y is None:
                continue

            self.console.print(
                projectile.x + MAP_OFFSET_X,
                projectile.y,
                projectile.glyph,
                fg=projectile.color,
            )

        # Targeting (se em modo de seleção de alvo)
        if engine.state == engine.GameState.TARGETING:
            self.console.print(
                int(engine.target_x) + MAP_OFFSET_X,
                int(engine.target_y),
                "X",
                fg=(255, 0, 0),
            )

        # Apresentar no contexto
        engine.context.present(self.console)