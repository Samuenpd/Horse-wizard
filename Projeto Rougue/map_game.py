class Tile:
    def __init__(self, walkable, transparent):
        self.walkable = walkable
        self.transparent = transparent

floor = Tile(True, True)
wall = Tile(False, False)

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[floor for y in range(height)] for x in range(width)]
