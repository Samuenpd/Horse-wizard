import tcod.event
from tcod.event import KeySym
from engine import GameState


MOVE_KEYS = {
    # WASD
    KeySym.W: (0, -1),
    KeySym.S: (0, 1),
    KeySym.A: (-1, 0),
    KeySym.D: (1, 0),

    # Setas
    KeySym.UP: (0, -1),
    KeySym.DOWN: (0, 1),
    KeySym.LEFT: (-1, 0),
    KeySym.RIGHT: (1, 0),
}


class EventHandler(tcod.event.EventDispatch):
    def __init__(self, engine):
        self.engine = engine

    # ======================
    # INPUT NORMAL (JOGO)
    # ======================
    def ev_keydown(self, event):
        key = event.sym

        # ---------- TARGETING ----------
        if self.engine.state == GameState.TARGETING:
            return self.handle_targeting_input(key)

        # ---------- MOVIMENTO ----------
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            self.engine.player.move(dx, dy, self.engine.game_map)
            return None

        # ---------- MENU DE MAGIAS ----------
        if key == KeySym.M:
            self.engine.toggle_spell_menu()
            return None

        # ---------- SELEÇÃO DE MAGIA (1–9) ----------
        if KeySym.N1 <= key <= KeySym.N9:
            slot = key - KeySym.N0
            spell = self.engine.player.spellbook.slots.get(slot)

            if spell:
                self.engine.start_targeting(spell)

        return None

    # ======================
    # INPUT DE MIRA
    # ======================
    def handle_targeting_input(self, key):
        cursor = self.engine.target_cursor

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            cursor.move(dx, dy)
            return None

        if key == KeySym.RETURN:
            self.engine.confirm_target()
            return None

        if key == KeySym.ESCAPE:
            self.engine.cancel_targeting()
            return None

        return None
