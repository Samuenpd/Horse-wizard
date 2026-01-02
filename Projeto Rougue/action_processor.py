import ai


class ActionProcessor:
    def __init__(self, engine):
        self.engine = engine

    def process(self, action):
        match action["type"]:

            case "move":
                self._process_move(action)

            case "select_spell":
                self._process_select_spell(action)

            case "confirm_target":
                self._process_confirm_target()

            case "cancel":
                self._process_cancel()

            case "mouse_move":
                self._process_mouse_move(action)

            case "quit":
                self._process_quit()

    def _end_player_turn(self):
        """Chamado após jogador realizar uma ação que custa turno"""
        self._process_enemy_turns()
        self._remove_dead_entities()

    def _process_move(self, action):
        # Movimento do jogador
        self.engine.player.move(
            action["dx"],
            action["dy"],
            self.engine.game_map,
            self.engine.entities,
            self.engine,
        )
        
        # Custa turno
        self._end_player_turn()

    def _process_enemy_turns(self):
        for entity in self.engine.entities:
            if entity is self.engine.player:
                continue
            if not hasattr(entity, "fighter"):
                continue

            # Delay opcional
            if hasattr(entity, "turn_delay"):
                entity.turn_counter += 1
                if entity.turn_counter < entity.turn_delay:
                    continue
                entity.turn_counter = 0

            ai.move_towards(
                entity,
                self.engine.player.x,
                self.engine.player.y,
                self.engine.game_map,
                self.engine.entities,
                self.engine,
            )

    def _remove_dead_entities(self):
        for entity in self.engine.entities[:]:
            if hasattr(entity, "fighter") and entity.fighter.hp <= 0:
                self.engine.entities.remove(entity)

    def _process_select_spell(self, action):
        spell = self.engine.player.spellbook.select(action["spell_id"])
        if spell and spell.requires_target:
            self.engine.state = self.engine.GameState.TARGETING
        else:
            self.engine.state = self.engine.GameState.PLAYING

    def _process_confirm_target(self):
        spell = self.engine.player.spellbook.active_spell
        if not spell:
            return

        if spell.requires_target and self.engine.state != self.engine.GameState.TARGETING:
            return

        # Verifica se tem mana suficiente
        if self.engine.player.mana < spell.cost:
            # Poderia adicionar uma mensagem "Mana insuficiente!"
            return

        # Gasta mana e casta a magia
        self.engine.player.mana -= spell.cost
        self.engine.player.spellbook.cast_active(
            self.engine,
            int(self.engine.target_x),
            int(self.engine.target_y),
        )
        
        # Custa turno
        self._end_player_turn()
        
        self.engine.state = self.engine.GameState.PLAYING

    def _process_cancel(self):
        self.engine.player.spellbook.active_spell = None
        self.engine.state = self.engine.GameState.PLAYING

    def _process_mouse_move(self, action):
        if self.engine.state == self.engine.GameState.TARGETING:
            map_x = action["x"] - self.engine.MAP_OFFSET_X
            map_y = action["y"]

            if self.engine.game_map.in_bounds(map_x, map_y):
                self.engine.target_x = map_x
                self.engine.target_y = map_y

    def _process_quit(self):
        self.engine.running = False