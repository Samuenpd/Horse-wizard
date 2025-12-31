import tcod
import tcod.event

from entity import Entity
from input_handlers import handle_event
from components.fighter import Fighter
from components.spells import MagicMissile


class Engine:
    def __init__(self, console):
        self.console = console
        self.context = None
        self.entities = []
        self.projectiles = []

        self.player = Entity(
            40, 22, "@", (255, 255, 255), "Player",
            blocks=True,
            fighter=Fighter(30, 5)
        )
        self.entities.append(self.player)

        orc = Entity(
            45, 22, "C", (255, 0, 0), "Cavalo",
            blocks=True,
            fighter=Fighter(10, 3)
        )
        self.entities.append(orc)

        self.spells = {
            "magic_missile": MagicMissile()
        }

        self.targeting = False
        self.target_spell = None
        self.mouse_position = (self.player.x, self.player.y)

    def run(self, context):
        self.context = context
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()

            self.context.convert_event(event)

            action = handle_event(event)
            if action:
                self.process_action(action)

    def process_action(self, action):
        t = action["type"]

        if t == "move":
            dx, dy = action["dx"], action["dy"]
            x = self.player.x + dx
            y = self.player.y + dy

            target = self.get_blocking_entity(x, y)
            if target and target.fighter:
                self.attack(self.player, target)
            else:
                self.player.move(dx, dy)

        elif t == "start_targeting":
            self.targeting = True
            self.target_spell = self.spells[action["spell"]]

        elif t == "mouse_move" and self.targeting:
            if action["x"] is not None and action["y"] is not None:
                self.mouse_position = (int(action["x"]), int(action["y"]))

        elif t == "mouse_click" and self.targeting:
            x, y = action["x"], action["y"]
            self.target_spell.cast(self, self.player, x, y)
            self.targeting = False
            self.target_spell = None

        elif t == "cancel_targeting":
            self.targeting = False
            self.target_spell = None

        elif t == "exit":
            raise SystemExit()

    def get_blocking_entity(self, x, y):
        for e in self.entities:
            if e.blocks and e.x == x and e.y == y:
                return e
        return None

    def attack(self, attacker, defender):
        dead = defender.fighter.take_damage(attacker.fighter.power)
        if dead:
            self.entities.remove(defender)

    def render(self):
        self.console.clear()

        for e in self.entities:
            self.console.print(e.x, e.y, e.glyph, fg=e.color)

        if self.targeting:
            mx, my = self.mouse_position

            if mx is not None and my is not None:
                path = tcod.los.bresenham(
                    (self.player.x, self.player.y),
                    (mx, my)
                ).tolist()
                for x, y in path:
                    self.console.print(x, y, "*", fg=(0, 255, 255))
        
        for p in self.projectiles:
            self.console.print(p.x, p.y, p.glyph, fg=p.color)

        self.context.present(self.console)

    def get_line(self, x1, y1, x2, y2):
        return tcod.los.bresenham((x1, y1), (x2, y2)).tolist()
    
    def update(self):
        for p in self.projectiles[:]:
            p.update()

            x, y = p.x, p.y

            target = self.get_blocking_entity(x, y)
            if target and target.fighter:
                dead = target.fighter.take_damage(p.damage)
                if dead:
                    if target in self.entities:
                        self.entities.remove(target)
                if p in self.projectiles:
                    self.projectiles.remove(p)
                continue

            if p.finished():
                if p in self.projectiles:
                    self.projectiles.remove(p)
