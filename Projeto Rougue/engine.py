import tcod.event
from input_handlers import handle_keys
from entity import Entity
from components.fighter import Fighter
from components.spells import Spell, MagicMissile

class Engine:
    def __init__(self, console):
        self.console = console
        self.entities = []
        self.spells = {
            "magic_missile": MagicMissile()
        }

        # PLAYER
        self.player = Entity(
            40, 22,
            "@",
            (255, 255, 255),
            "Player",
            blocks=True,
            fighter=Fighter(hp=30, power=5)
        )

        self.entities.append(self.player)

        # INIMIGO (Copia isso pra futuros inimigos blz?)        
        cavalo = Entity(
            43, 22,          # posição no mapa
            "C",             # Troca por png no futuro viu
            (0, 200, 0),    
            "Cavalo",      
            blocks=True,
            fighter=Fighter(hp=10, power=3)
        )

        self.entities.append(cavalo)

    def run(self, context):
        while True:
            self.render(context)
            self.handle_events()

    def handle_events(self):
        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()

            action = handle_keys(event)

            if action:
                self.process_action(action)

    def process_action(self, action):
        if action["type"] == "move":
            dx, dy = action["dx"], action["dy"]
            dest_x = self.player.x + dx
            dest_y = self.player.y + dy

            target = self.get_blocking_entity(dest_x, dest_y)

            if target and target.fighter:
                self.attack(self.player, target)
            else:
                self.player.move(dx, dy)

        elif action["type"] == "cast_spell":
            spell = self.spells[action["spell"]]

            # alvo simples (direita do player)
            target_x = self.player.x + 1
            target_y = self.player.y

            spell.cast(self, self.player, target_x, target_y)

    def get_blocking_entity(self, x, y):
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return entity
        return None
    
    def attack(self, attacker, defender):
        damage = attacker.fighter.power
        dead = defender.fighter.take_damage(damage)

        print(f"{attacker.name} ataca {defender.name} causando {damage} de dano!")

        if dead:
            print(f"{defender.name} morreu!")
            self.entities.remove(defender)

    def render(self, context):
        self.console.clear()

        for entity in self.entities:
            self.console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(self.console)
