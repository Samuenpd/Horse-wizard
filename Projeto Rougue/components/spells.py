import tcod
from entity import Projectile


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
        super().__init__("Magic Missile", 8, 6)

    def cast(self, engine, caster, target_x, target_y):
        path = tcod.los.bresenham(
            (caster.x, caster.y),
            (target_x, target_y)
        ).tolist()

        if len(path) <= 1:
            return

        engine.projectiles.append(
            Projectile(path, self.damage)
        )
