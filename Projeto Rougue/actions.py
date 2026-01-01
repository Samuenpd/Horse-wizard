class Action:
    def perform(self, engine):
        raise NotImplementedError()


class CastSpellAction(Action):
    def __init__(self, caster, spell_name, target_x, target_y):
        self.caster = caster
        self.spell_name = spell_name
        self.target_x = target_x
        self.target_y = target_y

    def perform(self, engine):
        spell = engine.spell_library.get(self.spell_name)
        if not spell:
            return

        if self.caster.mana < spell.cost:
            return

        self.caster.mana -= spell.cost
        spell.cast(self.caster, engine, self.target_x, self.target_y)
