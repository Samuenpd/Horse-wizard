import random
from map_game import GameMap, Tile
from enemies import create_goblin, create_cavalo, create_mago


class RiftWizardGenerator:
    def __init__(self, width, height, num_rooms=6):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        
        # Tipos de sala temáticas
        self.room_types = [
            "goblin_den",      # Sala de goblins
            "knight_hall",     # Sala de cavalos
            "wizard_chamber",  # Sala de magos
            "mixed_force",     # Sala mista
            "treasure_room",   # Sala com tesouro (menos inimigos)
            "empty_hall",      # Sala vazia/descanso
        ]
    
    def generate(self):
        """Gera um mapa estilo Rift Wizard"""
        game_map = GameMap(self.width, self.height)
        
        # Inicializa tudo como parede
        for x in range(self.width):
            for y in range(self.height):
                game_map.tiles[x][y] = Tile(walkable=False)
        
        # Layout em grade 3x2 ou 2x3
        grid_cols = 3 if self.width > self.height else 2
        grid_rows = self.num_rooms // grid_cols
        
        # Calcula tamanho das células da grade
        cell_width = self.width // grid_cols
        cell_height = self.height // grid_rows
        
        rooms = []
        entities = []
        room_grid = {}  # (grid_x, grid_y) -> room_data
        
        # Cria salas na grade
        room_index = 0
        for gy in range(grid_rows):
            for gx in range(grid_cols):
                if room_index >= self.num_rooms:
                    break
                
                # Define área da sala (com margens)
                room_x = gx * cell_width + 2
                room_y = gy * cell_height + 2
                room_w = cell_width - 4
                room_h = cell_height - 4
                
                # Escolhe tipo de sala
                room_type = random.choice(self.room_types)
                
                # Cria a sala
                room_data = self._create_themed_room(
                    game_map, room_x, room_y, room_w, room_h, room_type
                )
                
                # Popula a sala
                room_entities = self._populate_room(
                    game_map, room_x, room_y, room_w, room_h, room_type
                )
                entities.extend(room_entities)
                
                # Guarda dados da sala
                rooms.append({
                    "grid_pos": (gx, gy),
                    "rect": (room_x, room_y, room_w, room_h),
                    "type": room_type,
                    "center": (room_x + room_w // 2, room_y + room_h // 2)
                })
                room_grid[(gx, gy)] = rooms[-1]
                
                room_index += 1
        
        # Conecta salas adjacentes na grade
        for room in rooms:
            gx, gy = room["grid_pos"]
            
            # Conecta com sala à direita
            if (gx + 1, gy) in room_grid:
                self._connect_rooms(game_map, room, room_grid[(gx + 1, gy)])
            
            # Conecta com sala abaixo
            if (gx, gy + 1) in room_grid:
                self._connect_rooms(game_map, room, room_grid[(gx, gy + 1)])
        
        # Primeira sala é onde o jogador começa (sala vazia se possível)
        start_room = None
        for room in rooms:
            if room["type"] == "empty_hall":
                start_room = room
                break
        
        if not start_room:
            start_room = rooms[0]
        
        player_start = start_room["center"]
        
        # Remove inimigos da sala inicial (se houver)
        entities = [e for e in entities 
                   if not (start_room["rect"][0] <= e.x < start_room["rect"][0] + start_room["rect"][2] and
                          start_room["rect"][1] <= e.y < start_room["rect"][1] + start_room["rect"][3])]
        
        # Adiciona portal de saída na última sala
        last_room = rooms[-1]
        exit_x, exit_y = last_room["center"]
        # (Podemos adicionar um objeto especial depois)
        
        return game_map, entities, player_start
    
    def _create_themed_room(self, game_map, x, y, w, h, room_type):
        """Cria uma sala com tema específico"""
        
        # Padrão base (sala retangular)
        for rx in range(x, x + w):
            for ry in range(y, y + h):
                if 0 <= rx < self.width and 0 <= ry < self.height:
                    game_map.tiles[rx][ry] = Tile(walkable=True)
        
        # Adiciona elementos baseados no tema
        if room_type == "goblin_den":
            # Sala bagunçada com obstáculos
            self._add_obstacles(game_map, x, y, w, h, density=0.15)
        
        elif room_type == "knight_hall":
            # Sala aberta (boa para cavalos se moverem)
            # Remove obstáculos do centro
            center_x, center_y = x + w//2, y + h//2
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    rx, ry = center_x + dx, center_y + dy
                    if x <= rx < x + w and y <= ry < y + h:
                        game_map.tiles[rx][ry] = Tile(walkable=True)
        
        elif room_type == "wizard_chamber":
            # Sala com pilares/cobertura
            self._add_pillars(game_map, x, y, w, h)
        
        elif room_type == "mixed_force":
            # Sala com algumas barricadas
            self._add_barricades(game_map, x, y, w, h)
        
        elif room_type == "treasure_room":
            # Sala com menos inimigos, talvez tesouro depois
            pass
        
        elif room_type == "empty_hall":
            # Sala completamente limpa
            pass
        
        return (x, y, w, h)
    
    def _add_obstacles(self, game_map, x, y, w, h, density=0.1):
        """Adiciona obstáculos aleatórios na sala"""
        num_obstacles = int(w * h * density)
        
        for _ in range(num_obstacles):
            ox = random.randint(x + 1, x + w - 2)
            oy = random.randint(y + 1, y + h - 2)
            
            # Pequenos grupos de obstáculos
            for dx in range(random.randint(1, 2)):
                for dy in range(random.randint(1, 2)):
                    rx, ry = ox + dx, oy + dy
                    if x <= rx < x + w and y <= ry < y + h:
                        game_map.tiles[rx][ry] = Tile(walkable=False)
    
    def _add_pillars(self, game_map, x, y, w, h):
        """Adiciona pilares estratégicos (cobertura para magos)"""
        if w > 6 and h > 6:
            # Pilares nos cantos
            positions = [
                (x + 2, y + 2),
                (x + w - 3, y + 2),
                (x + 2, y + h - 3),
                (x + w - 3, y + h - 3),
            ]
            
            for px, py in positions:
                game_map.tiles[px][py] = Tile(walkable=False)
                # Pequeno grupo 2x2
                for dx in range(2):
                    for dy in range(2):
                        rx, ry = px + dx, py + dy
                        if x <= rx < x + w and y <= ry < y + h:
                            game_map.tiles[rx][ry] = Tile(walkable=False)
    
    def _add_barricades(self, game_map, x, y, w, h):
        """Adiciona barricadas (paredes baixas)"""
        # Barricada horizontal ou vertical
        if random.random() < 0.5 and h > 5:
            # Horizontal
            bar_y = y + random.randint(2, h - 3)
            for bx in range(x + 1, x + w - 1):
                if random.random() < 0.7:  # Deixa alguns espaços
                    game_map.tiles[bx][bar_y] = Tile(walkable=False)
        elif w > 5:
            # Vertical
            bar_x = x + random.randint(2, w - 3)
            for by in range(y + 1, y + h - 1):
                if random.random() < 0.7:
                    game_map.tiles[bar_x][by] = Tile(walkable=False)
    
    def _populate_room(self, game_map, x, y, w, h, room_type):
        """Popula uma sala com inimigos baseado no tema"""
        entities = []
        
        # Define densidade e tipos baseado no tema
        if room_type == "goblin_den":
            num_enemies = random.randint(4, 8)
            enemy_pool = ["goblin"] * 8 + ["cavalo"] * 2
        
        elif room_type == "knight_hall":
            num_enemies = random.randint(3, 6)
            enemy_pool = ["cavalo"] * 7 + ["goblin"] * 3
        
        elif room_type == "wizard_chamber":
            num_enemies = random.randint(2, 4)
            enemy_pool = ["mago"] * 6 + ["goblin"] * 4
        
        elif room_type == "mixed_force":
            num_enemies = random.randint(5, 9)
            enemy_pool = ["goblin"] * 5 + ["cavalo"] * 3 + ["mago"] * 2
        
        elif room_type == "treasure_room":
            num_enemies = random.randint(1, 3)  # Menos inimigos
            enemy_pool = ["goblin"] * 5 + ["cavalo"] * 3 + ["mago"] * 2
        
        elif room_type == "empty_hall":
            num_enemies = 0  # Sala vazia
            enemy_pool = []
        
        # Posiciona inimigos
        for _ in range(num_enemies):
            placed = False
            attempts = 0
            
            while not placed and attempts < 20:
                ex = random.randint(x + 1, x + w - 2)
                ey = random.randint(y + 1, y + h - 2)
                
                if game_map.tiles[ex][ey].walkable:
                    # Verifica distância de outros inimigos na mesma sala
                    too_close = False
                    for entity in entities:
                        dist = abs(ex - entity.x) + abs(ey - entity.y)
                        if dist < 3:  # Espaçamento mínimo
                            too_close = True
                            break
                    
                    if not too_close:
                        enemy_type = random.choice(enemy_pool)
                        if enemy_type == "goblin":
                            enemy = create_goblin(ex, ey)
                        elif enemy_type == "cavalo":
                            enemy = create_cavalo(ex, ey)
                        else:  # mago
                            enemy = create_mago(ex, ey)
                        
                        entities.append(enemy)
                        placed = True
                
                attempts += 1
        
        return entities
    
    def _connect_rooms(self, game_map, room1, room2):
        """Conecta duas salas com um corredor"""
        x1, y1 = room1["center"]
        x2, y2 = room2["center"]
        
        # Corredor em L
        if random.random() < 0.5:
            # Horizontal primeiro
            self._carve_corridor(game_map, x1, x2, y1)
            self._carve_corridor(game_map, y1, y2, x2)
        else:
            # Vertical primeiro
            self._carve_corridor(game_map, y1, y2, x1)
            self._carve_corridor(game_map, x1, x2, y2)
    
    def _carve_corridor(self, game_map, start, end, fixed):
        """Cria um segmento de corredor"""
        step = 1 if end > start else -1
        for pos in range(start, end + step, step):
            if isinstance(fixed, int):  # Horizontal
                x, y = pos, fixed
            else:  # Vertical
                x, y = fixed, pos
            
            if 0 <= x < self.width and 0 <= y < self.height:
                game_map.tiles[x][y] = Tile(walkable=True)
                
                # Adiciona paredes laterais opcionais
                if random.random() < 0.3:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if not game_map.tiles[nx][ny].walkable:
                                game_map.tiles[nx][ny] = Tile(walkable=False)