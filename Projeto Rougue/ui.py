class UIPanel:
    def __init__(self, x: int, width: int, height: int):
        self.x = x
        self.width = width
        self.height = height

    def render(self, console, player, game_state):
        # fundo do painel
        for y in range(self.height):
            console.print(
                x=self.x,
                y=y,
                string=" " * self.width,
                bg=(20, 20, 20),
            )

        y = 1

        # título
        console.print(self.x + 1, y, "PLAYER", fg=(255, 255, 0))
        y += 2

        # HP
        console.print(
            self.x + 1,
            y,
            f"HP: {player.fighter.hp}",
            fg=(255, 80, 80),
        )
        y += 1

        # Mana
        if hasattr(player, "mana"):
            self.render_bar(
                console,
                self.x + 1,
                y,
                self.width - 2,
                player.mana,
                player.max_mana,
                fg=(0, 0, 120),
                bg=(0, 0, 40),
                label="MANA",
        )
        y += 2
        
        # Spell ativa
        console.print(self.x + 1, y, "SPELL", fg=(200, 200, 200))
        y += 1

        if player.spellbook.active_spell:
            spell = player.spellbook.active_spell
            console.print(
                self.x + 1,
                y,
                spell.name,
                fg=(255, 150, 0),
            )
        else:
            console.print(
                self.x + 1,
                y,
                "None",
                fg=(120, 120, 120),
            )
