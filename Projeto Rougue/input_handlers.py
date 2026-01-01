import tcod
import tcod.event


def handle_event(event):
    if isinstance(event, tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.W:
            return {"type": "move", "dx": 0, "dy": -1}

        if key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.S:
            return {"type": "move", "dx": 0, "dy": 1}

        if key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.A:
            return {"type": "move", "dx": -1, "dy": 0}

        if key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.D:
            return {"type": "move", "dx": 1, "dy": 0}

        if key == tcod.event.KeySym.ESCAPE:
            return {"type": "cancel"}

        if tcod.event.KeySym.N1 <= key <= tcod.event.KeySym.N9:
            return {
                "type": "select_spell",
                "spell_id": key - tcod.event.KeySym.N1
            }

    if isinstance(event, tcod.event.MouseMotion):
        if event.tile is not None:
            return {
                "type": "mouse_move",
                "x": int(event.tile.x),
                "y": int(event.tile.y),
            }

    if isinstance(event, tcod.event.MouseButtonDown):
        if event.button == 1:
            return {"type": "confirm_target"}

    return None
