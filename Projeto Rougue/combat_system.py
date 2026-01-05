class CombatSystem:
    def __init__(self, engine):
        self.engine = engine

    def update_projectiles(self):
        for projectile in self.engine.projectiles[:]:
            # Atualiza posição do projétil
            projectile.update()

            px, py = projectile.x, projectile.y
            
            # Verifica se está fora dos limites
            if not self.engine.game_map.in_bounds(px, py):
                self.engine.projectiles.remove(projectile)
                continue
                
            # Verifica se atingiu uma parede
            if not self.engine.game_map.tiles[px][py].walkable:
                self.engine.projectiles.remove(projectile)
                continue
            
            # Verifica se atingiu alguma entidade
            hit_entity = None
            
            for entity in self.engine.entities:
                # Verifica se a entidade está na posição do projétil
                if entity.x == px and entity.y == py:
                    if hasattr(entity, "fighter"):
                        # Causa dano
                        entity.fighter.take_damage(projectile.damage, self.engine)
                        hit_entity = entity
                        break
            
            # Remove projétil se atingiu algo
            if hit_entity:
                self.engine.projectiles.remove(projectile)
                continue
            
            # Remove projétil se terminou o trajeto
            if projectile.finished():
                self.engine.projectiles.remove(projectile)