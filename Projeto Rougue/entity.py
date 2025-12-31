class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, fighter=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter

        if self.fighter:
            self.fighter.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
