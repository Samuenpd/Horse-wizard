def move_towards(entity, target_x, target_y, game_map, entities):
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

    entity.move(dx, dy, game_map, entities)
