class CombatSystem:
    def __init__(self, engine):
        self.engine = engine

    def update_projectiles(self):
        for projectile in self.engine.projectiles[:]:
            projectile.update()

            px, py = projectile.x, projectile.y
            hit_entity = None

            for entity in self.engine.entities:
                if entity is self.engine.player:
                    continue

                if entity.x == px and entity.y == py and hasattr(entity, "fighter"):
                    entity.fighter.take_damage(projectile.damage, self.engine)

                    if entity.fighter.hp <= 0:
                        hit_entity = entity
                    break

            if hit_entity:
                self.engine.entities.remove(hit_entity)

            if hit_entity or projectile.finished():
                self.engine.projectiles.remove(projectile)