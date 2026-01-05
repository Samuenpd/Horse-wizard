import random
import math

def move_towards(entity, target_x, target_y, game_map, entities, engine):
    """Move entidade em direção ao alvo (para inimigos)"""
    dx = 0
    dy = 0

    if target_x > entity.x:
        dx = 1
    elif target_x < entity.x:
        dx = -1

    if target_y > entity.y:
        dy = 1
    elif target_y < entity.y:
        dy = -1

    # Usar movimento especial para inimigos que não ataca outros inimigos
    _enemy_move(entity, dx, dy, game_map, entities, engine)

def move_away(entity, target_x, target_y, game_map, entities, engine):
    """Move entidade para longe do alvo (para magos)"""
    dx = 0
    dy = 0

    if target_x > entity.x:
        dx = -1  # Move para longe
    elif target_x < entity.x:
        dx = 1   # Move para longe

    if target_y > entity.y:
        dy = -1  # Move para longe
    elif target_y < entity.y:
        dy = 1   # Move para longe

    # Tenta mover para longe
    _enemy_move(entity, dx, dy, game_map, entities, engine)

def _enemy_move(entity, dx, dy, game_map, entities, engine):
    """Movimento especial para inimigos que evita atacar outros inimigos"""
    new_x = entity.x + dx
    new_y = entity.y + dy

    if not (0 <= new_x < game_map.width and 0 <= new_y < game_map.height):
        return

    if not game_map.tiles[new_x][new_y].walkable:
        return

    # Verifica se há outra entidade na nova posição
    for other in entities:
        if other is entity:
            continue

        if other.x == new_x and other.y == new_y:
            # Só ataca o jogador, não outros inimigos
            if other is engine.player and hasattr(other, "fighter"):
                entity.attack(other, engine)
            return  # Para o movimento se houver qualquer entidade

    # Se chegou aqui, pode mover
    entity.x = new_x
    entity.y = new_y

def knight_move_towards(entity, target_x, target_y, game_map, entities, engine):
    """Move cavalo em L em direção ao alvo, mas pode atacar de casas adjacentes"""
    
    # PRIMEIRO: Verifica se o jogador está adjacente (pode atacar sem se mover)
    adjacent_positions = [
        (0, -1), (0, 1), (-1, 0), (1, 0),  # Cima, baixo, esquerda, direita
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonais
    ]
    
    for dx, dy in adjacent_positions:
        check_x = entity.x + dx
        check_y = entity.y + dy
        
        for other in entities:
            if other is engine.player and other.x == check_x and other.y == check_y:
                # Jogador está adjacente! Ataca imediatamente
                entity.attack(engine.player, engine)
                return True
    
    # SEGUNDO: Se não está adjacente, tenta se mover em L
    # Calcula a distância atual
    current_dist = math.sqrt((target_x - entity.x)**2 + (target_y - entity.y)**2)
    
    # Ordena os movimentos possíveis por proximidade ao alvo
    valid_moves = []
    
    for dx, dy in KNIGHT_MOVES:
        new_x = entity.x + dx
        new_y = entity.y + dy
        
        if not game_map.in_bounds(new_x, new_y):
            continue
            
        if not game_map.tiles[new_x][new_y].walkable:
            continue
            
        # Verifica se há outra entidade (exceto jogador)
        blocked = False
        for other in entities:
            if other is entity:
                continue
                
            if other.x == new_x and other.y == new_y:
                # Só considera bloqueado se não for o jogador
                if other is not engine.player:
                    blocked = True
                break
        
        if blocked:
            continue
        
        # Calcula nova distância
        new_dist = math.sqrt((target_x - new_x)**2 + (target_y - new_y)**2)
        
        # Prioriza movimentos que aproximam
        if new_dist < current_dist:
            valid_moves.append((new_dist, dx, dy, new_x, new_y, True))  # Aproxima
        else:
            valid_moves.append((new_dist, dx, dy, new_x, new_y, False))  # Não aproxima
    
    # Se houver movimentos válidos, escolhe o melhor
    if valid_moves:
        # Prioriza movimentos que aproximam
        valid_moves.sort(key=lambda x: (not x[5], x[0]))  # Primeiro os que aproximam, depois por distância
        
        for dist, dx, dy, new_x, new_y, aproxima in valid_moves:
            # Verifica se está indo para cima do jogador
            attacking_player = False
            for other in entities:
                if other is engine.player and other.x == new_x and other.y == new_y:
                    attacking_player = True
                    break
            
            if attacking_player:
                entity.attack(engine.player, engine)
            else:
                # Move para a posição
                entity.x = new_x
                entity.y = new_y
            return True
    
    # TERCEIRO: Se não conseguiu movimento em L, tenta movimento normal para se aproximar
    dx = 0
    dy = 0
    
    if target_x > entity.x:
        dx = 1
    elif target_x < entity.x:
        dx = -1
    
    if target_y > entity.y:
        dy = 1
    elif target_y < entity.y:
        dy = -1
    
    # Tenta movimento normal
    if dx != 0 or dy != 0:
        _enemy_move(entity, dx, dy, game_map, entities, engine)
        return True
    
    return False  # Não conseguiu se mover

def mago_behavior(entity, target_x, target_y, game_map, entities, engine):
    """Comportamento do mago: ataca à distância, mantém distância, com cast em 2 turnos"""
    
    # Calcula distância até o jogador
    distance = math.sqrt((target_x - entity.x)**2 + (target_y - entity.y)**2)
    
    # Reduz cooldown se necessário
    if hasattr(entity, "spell_cooldown") and entity.spell_cooldown > 0:
        entity.spell_cooldown -= 1
    
    # Verifica estado de casting
    is_casting = getattr(entity, "is_casting", False)
    casting_turn = getattr(entity, "casting_turn", 0)
    
    # 1. SE ESTÁ MUITO PERTO (< 3 tiles) → FUGE E CANCELA CAST
    if distance < 3:
        if is_casting:
            # Interrompe o cast se fugir
            entity.is_casting = False
            entity.casting_turn = 0
            if hasattr(entity, "original_color"):
                entity.color = entity.original_color
        
        move_away(entity, target_x, target_y, game_map, entities, engine)
        return True
    
    # 2. SE JÁ ESTÁ CASTANDO (segundo turno) → COMPLETA O CAST
    if is_casting and casting_turn >= 1:
        # Completa o cast e lança a magia
        entity.is_casting = False
        entity.casting_turn = 0
        
        # Lança a magia
        if _mago_complete_cast(entity, target_x, target_y, game_map, entities, engine):
            entity.spell_cooldown = 4  # Cooldown maior agora (4 turnos)
            
            # Volta à cor original
            if hasattr(entity, "original_color"):
                entity.color = entity.original_color
            
            return True
        else:
            # Se falhou o cast, volta à cor original
            if hasattr(entity, "original_color"):
                entity.color = entity.original_color
            
            # Tenta se mover lateralmente
            return _mago_move_lateral(entity, game_map, entities)
    
    # 3. SE PODE INICIAR UM NOVO CAST (na distância certa, com mana, sem cooldown)
    elif distance <= entity.spell_range and entity.mana >= 3 and entity.spell_cooldown <= 0:
        # Inicia o cast (primeiro turno)
        entity.is_casting = True
        entity.casting_turn = 1
        
        # Guarda a cor original se ainda não guardou
        if not hasattr(entity, "original_color"):
            entity.original_color = entity.color
        
        # Muda para cor de casting (amarelo brilhante)
        entity.color = (255, 255, 0)
        
        # Mostra texto de início de cast
        from floating_text import FloatingText
        engine.floating_texts.append(
            FloatingText(
                entity.x,
                entity.y,
                "CASTING...",
                (255, 255, 0)
            )
        )
        
        # Fica parado neste turno (preparando a magia)
        return True
    
    # 4. SE ESTÁ LONGE DEMAIS (> alcance) → SE APROXIMA UM POUCO
    elif distance > entity.spell_range:
        # Cancela qualquer cast se estiver se movendo
        if is_casting:
            entity.is_casting = False
            entity.casting_turn = 0
            if hasattr(entity, "original_color"):
                entity.color = entity.original_color
        
        # Move um pouco em direção ao jogador
        move_towards(entity, target_x, target_y, game_map, entities, engine)
        return True
    
    # 5. SE NÃO FEZ NADA AINDA → SE MOVE LATERALMENTE OU FICA PARADO
    else:
        # Cancela cast se estiver parado sem motivo
        if is_casting:
            entity.is_casting = False
            entity.casting_turn = 0
            if hasattr(entity, "original_color"):
                entity.color = entity.original_color
        
        return _mago_move_lateral(entity, game_map, entities)

def _mago_complete_cast(entity, target_x, target_y, game_map, entities, engine):
    """Completa o cast da magia (segundo turno)"""
    
    from entity import DirectionalProjectile
    
    # Escolhe tipo de magia aleatória
    spell_type = random.choice(["fire", "frost", "arcane"])
    
    # Configurações baseadas no tipo
    if spell_type == "fire":
        damage = 4
        glyph = "*"
        color = (255, 100, 0)  # Laranja
    elif spell_type == "frost":
        damage = 3
        glyph = "*"
        color = (100, 200, 255)  # Azul claro
    else:  # arcane
        damage = 3
        glyph = "*"
        color = (200, 50, 200)  # Roxo
    
    
    # Cria o projétil que passa pelo alvo e continua
    projectile = DirectionalProjectile(
        start_x=entity.x,
        start_y=entity.y,
        target_x=target_x,
        target_y=target_y,
        max_range=10,
        damage=damage,
        glyph=glyph,
        color=color,
        speed=0.7  # Mais lento para dar tempo de esquivar
    )
    engine.projectiles.append(projectile)
    
    # Gasta mana
    entity.mana -= 3
    
    # Adiciona texto flutuante de cast completo
    from floating_text import FloatingText
    engine.floating_texts.append(
        FloatingText(
            entity.x,
            entity.y,
            "CAST!",
            color
        )
    )
    
    return True

def _mago_move_lateral(entity, game_map, entities):
    """Move o mago lateralmente para reposicionamento"""
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(moves)
    
    for dx, dy in moves:
        new_x = entity.x + dx
        new_y = entity.y + dy
        
        if not game_map.in_bounds(new_x, new_y):
            continue
            
        if not game_map.tiles[new_x][new_y].walkable:
            continue
        
        # Verifica se a posição está livre
        blocked = False
        for other in entities:
            if other is entity:
                continue
                
            if other.x == new_x and other.y == new_y:
                blocked = True
                break
        
        if not blocked:
            entity.x = new_x
            entity.y = new_y
            return True
    
    # Se não conseguiu se mover lateralmente, fica parado
    return True

def knight_move_random(entity, game_map, entities, engine):
    """Movimento aleatório em L (mantido para compatibilidade)"""
    random.shuffle(KNIGHT_MOVES)

    for dx, dy in KNIGHT_MOVES:
        new_x = entity.x + dx
        new_y = entity.y + dy

        if not game_map.in_bounds(new_x, new_y):
            continue

        if not game_map.tiles[new_x][new_y].walkable:
            continue

        # Verifica se há outra entidade (exceto jogador)
        blocked = False
        for other in entities:
            if other is entity:
                continue
                
            if other.x == new_x and other.y == new_y:
                # Só bloqueia se não for o jogador
                if other is not engine.player:
                    blocked = True
                break
        
        if blocked:
            continue

        entity.x = new_x
        entity.y = new_y
        return

KNIGHT_MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
]