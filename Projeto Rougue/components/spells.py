from typing import Dict


class Spell:
    def __init__(self, spell_id, cost, requires_target=True):
        self.id = spell_id
        self.cost = cost
        self.requires_target = requires_target

    def cast(self, engine, x=None, y=None):
        raise NotImplementedError()



class Firebolt(Spell):
    def __init__(self):
        super().__init__(
            spell_id="firebolt",
            cost=5,
            requires_target=True,
        )

    def cast(self, engine, x, y):
        engine.console.print(x, y, "*", fg=(255, 0, 0))


class Heal(Spell):
    def __init__(self):
        super().__init__(
            spell_id="heal",
            cost=3,
            requires_target=False,
        )

    def cast(self, engine, x=None, y=None):
        engine.player.hp += 5
        engine.console.print(1, 2, "Você se curou!", fg=(0, 255, 0))



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
    def __init__(self):
        self.known = {}
        self.active_spell = None

    def learn(self, spell):
        self.known[spell.id] = spell

    def set_active(self, spell_id):
        if spell_id in self.known:
            self.active_spell = self.known[spell_id]

    def cast_active(self, engine, x, y):
        spell = self.active_spell
        player = engine.player

        if spell is None:
            return

        if player.mana < spell.cost:
            engine.console.print(1, 1, "Mana insuficiente", fg=(255, 0, 0))
            return

        player.mana -= spell.cost
        spell.cast(engine, x, y)
