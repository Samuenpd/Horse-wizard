class Fighter:
    def __init__(self, hp, power):
        self.max_hp = hp
        self.hp = hp
        self.power = power

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0
