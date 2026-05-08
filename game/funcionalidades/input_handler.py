def apply_zoom_keys(keys, zoom, pygame_module):
    if keys[pygame_module.K_q]:
        zoom += 0.01
    if keys[pygame_module.K_e]:
        zoom -= 0.01
    return zoom


def handle_state_event(event, game_state, level, player, vel_y, create_level_fn, pygame_module):
    if game_state == "menu" and event.type == pygame_module.KEYDOWN and event.key == pygame_module.K_RETURN:
        return game_state, level, vel_y, False, "game"

    if game_state == "menu" and event.type == pygame_module.KEYDOWN and event.key == pygame_module.K_ESCAPE:
        return game_state, level, vel_y, True, None

    if game_state == "win" and event.type == pygame_module.KEYDOWN and event.key == pygame_module.K_r:
        level = 1
        player.x, player.y = 100, 400
        vel_y = 0
        create_level_fn()
        return game_state, level, vel_y, False, "game"

    if game_state == "dead" and event.type == pygame_module.KEYDOWN and event.key == pygame_module.K_r:
        level = 1
        player.x, player.y = 100, 400
        vel_y = 0
        create_level_fn()
        return game_state, level, vel_y, False, "game"

    if game_state in ("win", "dead") and event.type == pygame_module.KEYDOWN and event.key == pygame_module.K_ESCAPE:
        return game_state, level, vel_y, True, None

    return game_state, level, vel_y, False, None
