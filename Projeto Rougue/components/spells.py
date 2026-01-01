from typing import Dict


def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return points


class Spell:
    def __init__(
        self,
        *,
        spell_id: str,
        name: str,
        cost: int,
        requires_target: bool,
    ):
        self.id = spell_id
        self.name = name
        self.cost = cost
        self.requires_target = requires_target

    def cast(self, engine, x=None, y=None):
        raise NotImplementedError()



class Firebolt(Spell):
    def __init__(self):
        super().__init__(
            spell_id="firebolt",
            name="Firebolt",
            cost=2,
            requires_target=True,
        )

    def cast(self, caster, engine, x, y):
        from entity import Projectile
        # Create projectile path from caster to target, skip caster tile
        path = bresenham_line(caster.x, caster.y, x, y)
        if len(path) <= 1:
            return
        path = path[1:]
        projectile = Projectile(path, damage=5, glyph="*", color=(255, 100, 0))
        engine.projectiles.append(projectile)



class Heal(Spell):
    def __init__(self):
        super().__init__(
            spell_id="heal",
            name="Heal",
            cost=3,
            requires_target=False,
        )

    def cast(self, caster, engine, x=None, y=None):
        caster.fighter.hp = min(
            caster.fighter.max_hp,
            caster.fighter.hp + 5
        )

class SpellLibrary:
    def __init__(self):
        self.spells = {}

    def register(self, spell):
        self.spells[spell.id] = spell

    def get(self, spell_id):
        return self.spells.get(spell_id)


def default_spell_library() -> SpellLibrary:
    lib = SpellLibrary()
    lib.register(Firebolt())
    lib.register(Heal())
    return lib

class Spellbook:
    def __init__(self, owner):
        self.owner = owner
        self.known = {}
        self.known_list = []  # Keep order of spells
        self.active_spell = None
        self.selected_index = 0

    def learn(self, spell: Spell):
        self.known[spell.id] = spell
        self.known_list.append(spell)

    def select(self, spell_index: int):
        if spell_index < 0 or spell_index >= len(self.known_list):
            return None

        self.selected_index = spell_index
        self.active_spell = self.known_list[spell_index]
        return self.active_spell

    def cast_active(self, engine, x=None, y=None):
        if not self.active_spell:
            return

        self.active_spell.cast(self.owner, engine, x, y)
        self.active_spell = None
