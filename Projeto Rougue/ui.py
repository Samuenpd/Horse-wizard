class UIPanel:
    def __init__(self, x, width, height):
        self.x = x
        self.width = width
        self.height = height

    def render(self, console, player, engine):  # ✅ Alterado de engine para engine
        console.draw_frame(
            x=self.x,
            y=0,
            width=self.width,
            height=self.height,
            title="PLAYER",
        )

        y = 2

        console.print(
            self.x + 1,
            y,
            "HP:",
            fg=(255, 0, 0),
        )
        console.print(
            self.x + 5,
            y,
            f"{player.fighter.hp} / {player.fighter.max_hp}",
            fg=(255, 255, 255),
        )
        y += 1

        if hasattr(player, "mana"):
            console.print(
                self.x + 1,
                y,
                "MANA:",
                fg=(0, 0, 255),
            )
            console.print(
                self.x + 5,
                y,
                f"{player.mana} / {player.max_mana}",
                fg=(255, 255, 255),
            )
            y += 2
        else:
            y += 1

        spell = player.spellbook.active_spell

        console.print(
            self.x + 1,
            y,
            "MAGIA:",
            fg=(255, 255, 0),
        )
        y += 1

        if spell:
            console.print(
                self.x + 1,
                y,
                spell.name,
                fg=(255, 255, 255),
            )
        else:
            console.print(
                self.x + 1,
                y,
                "Nenhuma",
                fg=(120, 120, 120),
            )
        y += 2

        spellbook = player.spellbook

        for i, s in enumerate(spellbook.known_list):
            prefix = ">" if i == spellbook.selected_index else " "
            color = (255, 255, 255)

            if i == spellbook.selected_index:
                color = (255, 255, 0)

            console.print(
                self.x + 1,
                y,
                f"{prefix} {i + 1}. {s.name}",
                fg=color,
            )
            y += 1