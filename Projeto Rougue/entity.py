class Entity:
    def __init__(self, x, y, glyph, color, name, blocks=False, fighter=None):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter

        if self.fighter:
            self.fighter.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Projectile:
    def __init__(self, path, damage, glyph="*", color=(255, 255, 0)):
        self.path = path
        self.index = 0
        self.damage = damage
        self.glyph = glyph
        self.color = color

    def update(self):
        self.index += 1

    @property
    def x(self):
        return self.path[self.index][0]

    @property
    def y(self):
        return self.path[self.index][1]

    def finished(self):
        return self.index >= len(self.path) - 1
