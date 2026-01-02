import random

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

KNIGHT_MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2),
]

def knight_move(entity, game_map, entities):
    random.shuffle(KNIGHT_MOVES)

    for dx, dy in KNIGHT_MOVES:
        new_x = entity.x + dx
        new_y = entity.y + dy

        if not game_map.in_bounds(new_x, new_y):
            continue

        if not game_map.tiles[new_x][new_y].walkable:
            continue

        if any(e.x == new_x and e.y == new_y for e in entities):
            continue

        entity.x = new_x
        entity.y = new_y
        return