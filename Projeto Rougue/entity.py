from components.fighter import Fighter
from components.spells import Spellbook

class Entity:
    def __init__(self, x, y, glyph, color, is_player=False):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color
        self.is_player = is_player

        self.fighter = Fighter(hp=10, power=3)

        if is_player:
            self.max_mana = 10
            self.mana = 10
            self.spellbook = Spellbook(self)
        else:
            self.spellbook = None

    def move(self, dx, dy, game_map, entities):
        new_x = self.x + dx
        new_y = self.y + dy

        # limites do mapa
        if not (0 <= new_x < game_map.width and 0 <= new_y < game_map.height):
            return

        # parede
        if not game_map.tiles[new_x][new_y].walkable:
            return

        # inimigos bloqueiam movimento
        for entity in entities:
            if entity is self:
                continue

            if entity.x == new_x and entity.y == new_y:
                if entity.fighter:
                    self.attack(entity)
                return

        # movimento permitido
        self.x = new_x
        self.y = new_y

    def draw(self, console):
        console.print(self.x, self.y, self.glyph, fg=self.color)

    def attack(self, target):
        if not self.fighter or not target.fighter:
            return

        damage = self.fighter.power
        target.fighter.take_damage(damage)

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
        if not self.path:
            return None
        return self.path[self.index][0]

    @property
    def y(self):
        if not self.path:
            return None
        return self.path[self.index][1]

    def finished(self):
        return self.index >= len(self.path) - 1