import tcod.event


def handle_event(event):
    if event.type == "KEYDOWN":
        key = event.sym

        if key == tcod.event.KeySym.UP or key == tcod.event.KeySym.w:
            return {"type": "move", "dx": 0, "dy": -1}
        if key == tcod.event.KeySym.DOWN or key == tcod.event.KeySym.s:
            return {"type": "move", "dx": 0, "dy": 1}
        if key == tcod.event.KeySym.LEFT or key == tcod.event.KeySym.a:
            return {"type": "move", "dx": -1, "dy": 0}
        if key == tcod.event.KeySym.RIGHT or key == tcod.event.KeySym.d:
            return {"type": "move", "dx": 1, "dy": 0}

        if key == tcod.event.KeySym.m:
            return {
                "type": "start_targeting",
                "spell": "magic_missile"
            }

        if key == tcod.event.KeySym.ESCAPE:
            return {"type": "exit"}

    if event.type == "MOUSEMOTION":
        return {
            "type": "mouse_move",
            "x": event.tile.x,
            "y": event.tile.y
        }

    if event.type == "MOUSEBUTTONDOWN":
        if event.button == 1:
            return {
                "type": "mouse_click",
                "x": event.tile.x,
                "y": event.tile.y
            }

        if event.button == 3:
            return {"type": "cancel_targeting"}

    return None