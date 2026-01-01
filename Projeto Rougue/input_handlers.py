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

        if key == tcod.event.KeySym.M:
            return {"type": "open_spell_menu"}

        if key == tcod.event.KeySym.ESCAPE:
            return {"type": "cancel"}

        if tcod.event.KeySym.N1 <= key <= tcod.event.KeySym.N9:
            spell_index = key - tcod.event.KeySym.N1
            # Get spell_id from the spell list (you may need to adjust this based on your needs)
            return {"type": "select_spell", "spell_id": spell_index}

    if isinstance(event, tcod.event.MouseMotion):
        return {"type": "mouse_move", "x": event.tile.x, "y": event.tile.y}

    if isinstance(event, tcod.event.MouseButtonDown):
        if event.button == 1:
            return {"type": "confirm_target"}

    return None
