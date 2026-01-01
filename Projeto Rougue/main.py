import tcod

from engine import Engine
from input_handlers import EventHandler
from map_game import GameMap
from entity import Entity
from components.spells import default_spell_library


def main():
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Projeto Rogue",
        vsync=True,
    ) as context:
        console = tcod.Console(screen_width, screen_height)

        game_map = GameMap(screen_width, screen_height)

        player = Entity(40, 25, "@", (255, 255, 255), is_player=True)
        entities = [player]

        spell_library = default_spell_library()

        engine = Engine(
            entities=entities,
            game_map=game_map,
            context=context,
            console=console,
            spell_library=spell_library,
        )

        event_handler = EventHandler(engine)

        while True:
            console.clear()
            engine.render()
            context.present(console)

            for event in tcod.event.wait():
                event_handler.dispatch(event)


if __name__ == "__main__":
    main()
