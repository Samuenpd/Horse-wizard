from components.fighter import Fighter
from components.spells import Spellbook, bresenham_line
import math

class Entity:
    def __init__(self, x, y, glyph, color, is_player=False):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color
        self.is_player = is_player

        self.fighter = Fighter(hp=25, power=3)
        self.fighter.entity = self

        if is_player:
            self.max_mana = 50
            self.mana = 50
            self.spellbook = Spellbook(self)
        else:
            self.spellbook = None

    def move(self, dx, dy, game_map, entities, engine):
        new_x = self.x + dx
        new_y = self.y + dy

        if not (0 <= new_x < game_map.width and 0 <= new_y < game_map.height):
            return

        if not game_map.tiles[new_x][new_y].walkable:
            return

        for entity in entities:
            if entity is self:
                continue

            if entity.x == new_x and entity.y == new_y:
                if entity.fighter:
                    self.attack(entity, engine) 
                return

        self.x = new_x
        self.y = new_y

    def draw(self, console):
        console.print(self.x, self.y, self.glyph, fg=self.color)

    def attack(self, target, engine): 
        if not self.fighter or not target.fighter:
            return

        damage = self.fighter.power
        target.fighter.take_damage(damage, engine)


class DirectionalProjectile:
    """Projétil que usa bresenham_line e se move mais devagar"""
    def __init__(self, start_x, start_y, target_x, target_y, max_range=15, damage=5, glyph="*", color=(255, 255, 0), speed=0.7):
        # Gera caminho até o alvo
        path_to_target = bresenham_line(start_x, start_y, target_x, target_y)
        
        # Remove o primeiro ponto (posição do atirador)
        if len(path_to_target) > 0:
            path_to_target = path_to_target[1:]
        
        # Se o caminho é muito curto, cria direção padrão
        if len(path_to_target) == 0:
            path_to_target = [(start_x + 1, start_y)]
        
        # Estende o caminho além do alvo
        self.path = self._extend_path(start_x, start_y, path_to_target, max_range)
        
        self.index = 0
        self.damage = damage
        self.glyph = glyph
        self.color = color
        self.target_index = len(path_to_target) - 1  # Índice do ponto alvo
        
        # Sistema de velocidade mais lenta
        self.speed = 0.7  # Tiles por turno (mais devagar que 1.0)
        self.move_accumulator = 0.0  # Acumulador para movimento fracionado
    
    def _extend_path(self, start_x, start_y, path_to_target, max_range):
        """Estende o caminho na mesma direção além do alvo"""
        if len(path_to_target) < 2:
            # Se não tem direção clara, vai para a direita
            extended = [(start_x + i + 1, start_y) for i in range(max_range)]
            return extended
        
        # Pega os últimos 2 pontos para determinar direção
        last = path_to_target[-1]
        
        # Para determinar direção precisa, usa os últimos pontos
        # Se só tem 1 ponto, usa direção do início
        if len(path_to_target) == 1:
            second_last = (start_x, start_y)
        else:
            second_last = path_to_target[-2]
        
        # Calcula direção
        dx = last[0] - second_last[0]
        dy = last[1] - second_last[1]
        
        # Normaliza para -1, 0, 1 mas mantém a direção
        if dx != 0:
            dx = 1 if dx > 0 else -1
        if dy != 0:
            dy = 1 if dy > 0 else -1
        
        # Começa com o caminho até o alvo
        extended_path = path_to_target[:]
        current = last
        
        # Continua até atingir max_range
        while len(extended_path) < max_range:
            next_x = current[0] + dx
            next_y = current[1] + dy
            extended_path.append((next_x, next_y))
            current = (next_x, next_y)
        
        return extended_path
    
    def update(self):
        # Sistema de movimento fracionado para velocidade < 1.0
        self.move_accumulator += self.speed
        
        # Move quando acumulou pelo menos 1.0
        while self.move_accumulator >= 1.0 and self.index < len(self.path) - 1:
            self.index += 1
            self.move_accumulator -= 1.0
    
    @property
    def x(self):
        if self.index >= len(self.path):
            return None
        return self.path[self.index][0]
    
    @property
    def y(self):
        if self.index >= len(self.path):
            return None
        return self.path[self.index][1]
    
    def finished(self):
        return self.index >= len(self.path) - 1
    
    def has_passed_target(self):
        return self.index >= self.target_index