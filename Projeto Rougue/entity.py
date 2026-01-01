from components.spells import Spellbook


class Entity:
    def __init__(self, x, y, glyph, color, is_player=False):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color

        self.hp = 10
        self.mana = 100

        self.is_player = is_player
        self.spellbook = Spellbook(self)

    def move(self, dx, dy, game_map):
        nx = self.x + dx
        ny = self.y + dy

        if not game_map.is_blocked(nx, ny):
            self.x = nx
            self.y = ny

    def draw(self, console):
        console.print(self.x, self.y, self.glyph, fg=self.color)

class Projectile:
    def __init__(self, path, damage, glyph="*", color=(255, 255, 0)):
        self.path = path
        self.index = 0
        self.damage = damage
        self.glyph = glyph
        self.color = color

    def update(self):
        if self.index < len(self.path) - 1:
            self.index += 1

    @property
    def x(self):
        return self.path[self.index][0]

    @property
    def y(self):
        return self.path[self.index][1]

    def finished(self):
        return self.index >= len(self.path) - 1