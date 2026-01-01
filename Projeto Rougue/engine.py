import tcod
import tcod.event

from input_handlers import handle_playing, handle_targeting


class GameState:
	PLAYING = 1
	MENU = 2
	TARGETING = 3


class Engine:
	def __init__(self, *, entities, game_map, player, context, console):
		self.entities = entities
		self.game_map = game_map
		self.player = player
		self.context = context
		self.console = console

		self.state = GameState.PLAYING
		self.running = True

		self.target_x = player.x
		self.target_y = player.y

	def run(self):
		while self.running:
			self.render()

			for event in tcod.event.wait():
				self.context.convert_event(event)

				if isinstance(event, tcod.event.Quit):
					self.running = False
					return

				self.handle_event(event)

	def handle_event(self, event):
		if self.state == GameState.PLAYING:
			action = handle_playing(event)

		elif self.state == GameState.TARGETING:
			action = handle_targeting(event)

		else:
			action = None

		if action:
			self.process_action(action)

	def process_action(self, action):
		kind = action[0]

		if kind == "move":
			_, dx, dy = action
			self.player.move(dx, dy, self.game_map)

		elif kind == "target":
			self.state = GameState.TARGETING
			self.target_x = self.player.x
			self.target_y = self.player.y

		elif kind == "aim":
			_, x, y = action
			self.target_x = x
			self.target_y = y

		elif kind == "cast":
			self.player.spellbook.cast_active(
				self,
				self.target_x,
				self.target_y
			)
			self.state = GameState.PLAYING

		elif kind == "cancel":
			self.state = GameState.PLAYING

		elif kind == "quit":
			self.running = False

	def render(self):
		self.console.clear()

		self.game_map.render(self.console)

		for entity in self.entities:
			self.console.print(
				entity.x,
				entity.y,
				entity.glyph,
				fg=entity.color
			)

		if self.state == GameState.TARGETING:
			self.console.print(
				self.target_x,
				self.target_y,
				"X",
				fg=(255, 0, 0)
			)

		self.context.present(self.console)
