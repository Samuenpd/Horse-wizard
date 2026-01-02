class FloatingText:
    def __init__(self, x, y, text, color, lifetime=20):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime

    def update(self):
        self.y -= 0.05        
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0