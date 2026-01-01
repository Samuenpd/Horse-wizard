class UIPanel:
    def __init__(self, x, width, height):
        self.x = x
        self.width = width
        self.height = height

    def render_bar(
        self,
        console,
        x,
        y,
        width,
        current,
        maximum,
        name,
        bar_color,
        back_color,
    ):
        if maximum <= 0:
            return

        ratio = current / maximum
        fill_width = int(width * ratio)

        # fundo
        console.draw_rect(
            x=x,
            y=y,
            width=width,
            height=1,
            ch=0,
            bg=back_color,
        )

        # barra cheia
        if fill_width > 0:
            console.draw_rect(
                x=x,
                y=y,
                width=fill_width,
                height=1,
                ch=0,
                bg=bar_color,
            )

        console.print(
            x + 1,
            y,
            f"{name}: {current}/{maximum}",
            fg=(255, 255, 255),
        )

    def render(self, console, player, state):
        console.draw_frame(
        x=self.x,
        y=0,
        width=self.width,
        height=self.height,
        title="PLAYER",
        )

        y = 2

        # HP
        self.render_bar(
            console,
            self.x + 1,
            y,
            self.width - 2,
            player.fighter.hp,
            player.fighter.max_hp,
            "HP",
            bar_color=(200, 0, 0),
            back_color=(60, 0, 0),
        )
        y += 2

        # MANA (só se existir)
        if hasattr(player, "mana"):
            self.render_bar(
                console,
                self.x + 1,
                y,
                self.width - 2,
                player.mana,
                player.max_mana,
                "MANA",
                bar_color=(0, 0, 200),
                back_color=(0, 0, 60),
            )
