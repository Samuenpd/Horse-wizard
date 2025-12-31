import tcod
from engine import Engine

def main():
    screen_width = 80
    screen_height = 50

    try:
        tileset = tcod.tileset.load_tilesheet(
            "assets/ibm437_font_8_8_bold.png",
            16,
            16,
            tcod.tileset.CHARMAP_CP437
        )
    except (OSError, RuntimeError):
        tileset = tcod.tileset.load_tilesheet(
            "assets/dejavu16x16_gs_tc.png",
            16,
            16,
            tcod.tileset.CHARMAP_CP437
        )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Horse Wizard",
        vsync=True,
    ) as context:

        console = tcod.Console(screen_width, screen_height, order="F")

        engine = Engine(console)
        engine.run(context)

if __name__ == "__main__":
    main()
