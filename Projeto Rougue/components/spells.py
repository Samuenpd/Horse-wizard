from typing import Dict


class Spell:
    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    def cast(self, caster, engine, x=None, y=None):
        raise NotImplementedError()


class Firebolt(Spell):
    def __init__(self):
        super().__init__("firebolt", cost=2)

    def cast(self, caster, engine, x, y):
        for entity in engine.entities:
            if entity.x == x and entity.y == y:
                if hasattr(entity, "hp"):
                    entity.hp -= 5


class Heal(Spell):
    def __init__(self):
        super().__init__("heal", cost=3)

    def cast(self, caster, engine, x=None, y=None):
        if hasattr(caster, "hp"):
            caster.hp += 5


class SpellLibrary:
    def __init__(self):
        self.spells: Dict[str, Spell] = {}

    def register(self, spell: Spell):
        self.spells[spell.name] = spell

    def get(self, name: str):
        return self.spells.get(name)


def default_spell_library() -> SpellLibrary:
    lib = SpellLibrary()
    lib.register(Firebolt())
    lib.register(Heal())
    return lib

class Spellbook:
    def __init__(self):
        self.known_spells: list[str] = []
        self.slots: dict[int, str | None] = {
            1: None,
            2: None,
            3: None,
            4: None,
        }

    def learn(self, spell_name: str):
        if spell_name not in self.known_spells:
            self.known_spells.append(spell_name)

    def equip(self, slot: int, spell_name: str):
        if spell_name in self.known_spells:
            self.slots[slot] = spell_name
