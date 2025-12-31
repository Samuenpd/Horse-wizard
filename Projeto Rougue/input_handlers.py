import tcod.event

def handle_keys(event):
    if event.type != "KEYDOWN":
        return None

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
        return {"type": "cast_spell", "spell": "magic_missile"}

    if key == tcod.event.KeySym.ESCAPE:
        raise SystemExit()
    
    return None


