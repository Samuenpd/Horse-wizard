class Tile:
	def __init__(self, walkable: bool):
		self.walkable = walkable


class GameMap:
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

		self.tiles = [
			[Tile(walkable=True) for _ in range(height)]
			for _ in range(width)
		]

		for y in range(self.height):
			for x in range(self.width):
				if (
					x == 0
					or y == 0
					or x == self.width - 1
					or y == self.height - 1
				):
					self.tiles[x][y].walkable = False

	def is_blocked(self, x: int, y: int) -> bool:
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return True

		return not self.tiles[x][y].walkable

	def render(self, console):
		for y in range(self.height):
			for x in range(self.width):
				if self.tiles[x][y].walkable:
					console.print(
						x=x,
						y=y,
						string="",
						fg=(40, 40, 40)
					)
				else:
					console.print(
						x=x,
						y=y,
						string="#",
						fg=(120, 120, 120)
					)

	def in_bounds(self, x: int, y: int) -> bool:
		return 0 <= x < self.width and 0 <= y < self.height