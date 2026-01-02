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

    # controle de turnos
    goblin.turn_delay = 2
    goblin.turn_counter = 0

    return goblin

def create_cavalo(x: int, y: int) -> Entity:
    fighter = Fighter(hp=3, power=5)

    cavalo = Entity(
        x=x,
        y=y,
        glyph="c",
        color=(137, 81, 41),
    )

    cavalo.fighter = fighter
    # controle de turnos
    cavalo.turn_delay = 1
    cavalo.turn_counter = 0

    return cavalo