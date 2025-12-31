class Spell:
    def __init__(self, name, range, damage, radius=0):
        self.name = name
        self.range = range
        self.damage = damage
        self.radius = radius

    def cast(self, engine, caster, target_x, target_y):
        raise NotImplementedError()
    
class MagicMissile(Spell):
    def __init__(self):
        super().__init__(
            name="Magic Missile",
            range=5,
            damage=6
        )

    def cast(self, engine, caster, target_x, target_y):
        target = engine.get_blocking_entity(target_x, target_y)

        if target and target.fighter:
            target.fighter.take_damage(self.damage)
            print(f"{caster.name} lança {self.name} em {target.name}!")
