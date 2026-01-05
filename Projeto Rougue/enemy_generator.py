import random
from enemies import create_goblin, create_cavalo, create_mago  # Adicionar create_mago


class EnemyGenerator:
    def __init__(self, game_map, max_enemies=10, spawn_distance=5):
        self.game_map = game_map
        self.max_enemies = max_enemies
        self.spawn_distance = spawn_distance  # Distância mínima do jogador
        self.enemy_types = [
            ("goblin", create_goblin, 0.5),
            ("cavalo", create_cavalo, 0.3),
            ("mago", create_mago, 0.2),       
        ]
    
    def find_valid_position(self, player_x, player_y, entities):
        """Encontra uma posição válida para spawnar inimigo"""
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            x = random.randint(1, self.game_map.width - 2)
            y = random.randint(1, self.game_map.height - 2)
            
            # Verifica se está longe o suficiente do jogador
            distance_to_player = abs(x - player_x) + abs(y - player_y)
            if distance_to_player < self.spawn_distance:
                attempts += 1
                continue
            
            # Verifica se a posição é walkable
            if not self.game_map.tiles[x][y].walkable:
                attempts += 1
                continue
            
            # Verifica se não há outra entidade na posição
            occupied = False
            for entity in entities:
                if entity.x == x and entity.y == y:
                    occupied = True
                    break
            
            if occupied:
                attempts += 1
                continue
            
            # Posição válida encontrada!
            return x, y
        
        # Não encontrou posição válida
        return None, None
    
    def spawn_random_enemy(self, player_x, player_y, entities):
        """Spawna um inimigo aleatório"""
        if len([e for e in entities if e.glyph in ["g", "c", "m"]]) >= self.max_enemies:
            return None  # Limite de inimigos atingido
        
        x, y = self.find_valid_position(player_x, player_y, entities)
        if x is None or y is None:
            return None  # Não encontrou posição válida
        
        # Escolhe tipo de inimigo baseado em pesos
        total_weight = sum(weight for _, _, weight in self.enemy_types)
        r = random.random() * total_weight
        
        current_weight = 0
        for enemy_type, creator, weight in self.enemy_types:
            current_weight += weight
            if r < current_weight:
                enemy = creator(x, y)
                
                # Adiciona alguma variação aleatória (opcional)
                if random.random() < 0.3:
                    self._add_variation(enemy, enemy_type)
                
                return enemy
        
        # Fallback
        return create_goblin(x, y)
    
    def _add_variation(self, enemy, enemy_type):
        """Adiciona variações aleatórias aos inimigos"""
        variations = [
            ("health", lambda: random.randint(2, 5)),
            ("power", lambda: random.randint(1, 3)),
            ("speed", lambda: random.uniform(0.5, 2.0)),
        ]
        
        # Escolhe uma variação aleatória
        variation_type, value_func = random.choice(variations)
        
        if variation_type == "health":
            bonus = value_func()
            enemy.fighter.max_hp += bonus
            enemy.fighter.hp += bonus
            
        elif variation_type == "power":
            bonus = value_func()
            enemy.fighter.power += bonus
            
        elif variation_type == "speed":
            speed_multiplier = value_func()
            if hasattr(enemy, "turn_delay"):
                # Ajusta o delay baseado no multiplicador
                enemy.turn_delay = max(1, int(enemy.turn_delay / speed_multiplier))
        
        # Variações específicas para mago
        if enemy_type == "mago" and random.random() < 0.5:
            if hasattr(enemy, "max_mana"):
                enemy.max_mana += random.randint(2, 5)
                enemy.mana = enemy.max_mana
    
    def spawn_wave(self, player_x, player_y, entities, wave_size=3):
        """Spawna uma onda de inimigos"""
        spawned = []
        for _ in range(wave_size):
            enemy = self.spawn_random_enemy(player_x, player_y, entities)
            if enemy:
                entities.append(enemy)
                spawned.append(enemy)
        return spawned
    
    def spawn_near_player(self, player_x, player_y, entities, radius=3):
        """Spawna inimigos perto do jogador (para teste)"""
        valid_positions = []
        
        # Procura posições válidas ao redor do jogador
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue  # Não spawnar em cima do jogador
                
                x = player_x + dx
                y = player_y + dy
                
                if not self.game_map.in_bounds(x, y):
                    continue
                
                if not self.game_map.tiles[x][y].walkable:
                    continue
                
                # Verifica se a posição está livre
                occupied = False
                for entity in entities:
                    if entity.x == x and entity.y == y:
                        occupied = True
                        break
                
                if not occupied:
                    valid_positions.append((x, y))
        
        if not valid_positions:
            return []
        
        # Escolhe posições aleatórias
        spawn_count = min(len(valid_positions), 2)  # No máximo 2 inimigos
        random.shuffle(valid_positions)
        positions = valid_positions[:spawn_count]
        
        spawned = []
        for x, y in positions:
            # Escolhe tipo baseado em pesos
            total_weight = sum(weight for _, _, weight in self.enemy_types)
            r = random.random() * total_weight
            
            current_weight = 0
            for enemy_type, creator, weight in self.enemy_types:
                current_weight += weight
                if r < current_weight:
                    enemy = creator(x, y)
                    entities.append(enemy)
                    spawned.append(enemy)
                    break
        
        return spawned