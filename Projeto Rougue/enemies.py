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
    fighter.entity = goblin 

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
    fighter.entity = cavalo  
    
    # controle de turnos
    cavalo.turn_delay = 1
    cavalo.turn_counter = 0
    
    # Adiciona um atributo para identificar o tipo de movimento
    cavalo.movement_type = "knight"  
    
    return cavalo

def create_mago(x: int, y: int) -> Entity:
    fighter = Fighter(hp=8, power=1)  # Menos HP, menos dano corpo-a-corpo

    mago = Entity(
        x=x,
        y=y,
        glyph="m",  # "m" para mago
        color=(150, 0, 200),  # Roxo
        is_player=False,
    )

    mago.fighter = fighter
    fighter.entity = mago
    
    # Atributos específicos do mago
    mago.max_mana = 15
    mago.mana = 15
    mago.spell_cooldown = 0  # Cooldown entre magias
    mago.spell_range = 6  # Alcance das magias
    
    # Sistema de cast em 2 turnos
    mago.is_casting = False  # Indica se está lançando magia
    mago.casting_turn = 0    # Contador de turnos de cast
    mago.original_color = (150, 0, 200)  # Cor original (roxo)
    
    # controle de turnos
    mago.turn_delay = 2
    mago.turn_counter = 0
    
    return mago