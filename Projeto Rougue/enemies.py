from entity import Entity
from components.fighter import Fighter


def create_goblin(x: int, y: int) -> Entity:
    fighter = Fighter(hp=10, power=3)

    goblin = Entity(
        x=x,
        y=y,
        glyph="g",
        color=(0, 200, 0),
    )

    goblin.fighter = fighter

    # CONTROLE DE TURNOS
    goblin.turn_delay = 2   # age a cada 2 turnos
    goblin.turn_counter = 0

    return goblin

