import tcod
import tcod.event


def handle_playing(event):
	if not isinstance(event, tcod.event.KeyDown):
		return None

	key = event.sym

	if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.W:
		return ("move", 0, -1)
	elif key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.S:
		return ("move", 0, 1)
	elif key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.A:
		return ("move", -1, 0)
	elif key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.D:
		return ("move", 1, 0)

	elif key == tcod.event.KeySym.M:
		return ("target",)

	elif key == tcod.event.KeySym.ESCAPE:
		return ("quit",)

	return None


def handle_targeting(event):
	if isinstance(event, tcod.event.MouseMotion):
		return ("aim", int(event.tile.x), int(event.tile.y))

	elif isinstance(event, tcod.event.MouseButtonDown):
		if event.button == 1:
			return ("cast",)

	elif isinstance(event, tcod.event.KeyDown):
		if event.sym == tcod.event.KeySym.ESCAPE:
			return ("cancel",)

	return None
