from floating_text import FloatingText


class Fighter:
    def __init__(self, hp: int, power: int):
        self.max_hp = hp
        self.hp = hp
        self.power = power
        self.entity = None 

    def take_damage(self, amount: int, engine):
        if amount <= 0:
            return

        self.hp = max(0, self.hp - amount)

        if self.entity:
            engine.floating_texts.append(
                FloatingText(
                    self.entity.x,
                    self.entity.y,
                    f"-{amount}",
                    (255, 60, 60)
                )
            )

        if self.hp == 0:
            self.die(engine)

    def heal(self, amount: int, engine):
        if amount <= 0:
            return

        healed = min(amount, self.max_hp - self.hp)
        if healed <= 0:
            return

        self.hp += healed

        if self.entity:
            engine.floating_texts.append(
                FloatingText(
                    self.entity.x,
                    self.entity.y,
                    f"+{healed}",
                    (60, 255, 60)
                )
            )

    def die(self, engine):
        if self.entity:
            self.entity.glyph = "%"
            self.entity.color = (120, 120, 120)