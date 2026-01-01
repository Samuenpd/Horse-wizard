import tcod

from engine import Engine
from entity import Entity
from map_game import GameMap
from components.spells import Spellbook, Firebolt, Heal
from enemies import create_goblin


def main():
    screen_width = 100
    screen_height = 50

    with tcod.context.new_terminal(
        columns=screen_width,
        rows=screen_height,
        tileset=tcod.tileset.load_tilesheet(
            "assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        ),
        title="Projeto Rogue",
        vsync=True,
    ) as context:

        console = tcod.console.Console(screen_width, screen_height)

        UI_WIDTH = 20
        MAP_WIDTH = screen_width - UI_WIDTH
        MAP_HEIGHT = screen_height

        game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

        player = Entity(
            x=screen_width // 2,
            y=screen_height // 2,
            glyph="@",
            color=(255, 255, 255),
            is_player=True,
        )

        player.spellbook = Spellbook(player)
        player.spellbook.learn(Firebolt())
        player.spellbook.learn(Heal())

        goblin = create_goblin(10, 10)

        entities = [player, goblin]

        engine = Engine(
            entities=entities,
            game_map=game_map,
            player=player,
            context=context,
            console=console,
        )

        engine.run()


if __name__ == "__main__":
    main()
