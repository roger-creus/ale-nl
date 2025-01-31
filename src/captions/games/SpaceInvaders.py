from ocatari.ram.game_objects import NoObject
from ocatari.ram.spaceinvaders import Player, Alien, Satellite, Shield, Bullet
from IPython import embed

def make_caption(ram, objs):
    ram_mappings = dict(
        invaders_left_count=17,
        num_lives=73,
    )
    
    # ram information
    caption = f"""
        Lives: {ram[ram_mappings['num_lives']]} \n
        Aliens left: {ram[ram_mappings['invaders_left_count']]} \n
        """
    
    # object information
    clsses = {Player, Alien, Satellite, Shield, Bullet}
    objs = {cls.__name__ : [obj for obj in objs if obj.__class__ == cls] for cls in clsses}
    
    # sort each item by x and y coordinates
    for cls, o in objs.items():
        objs[cls] = sorted(o, key=lambda x: x.center[0])
        objs[cls] = sorted(o, key=lambda x: x.center[1])

    aliens = objs['Alien']
    del objs['Alien']
    
    for cls, o in objs.items():
        if len(o) > 0:
            c = 0
            for obj in o:
                if obj.__class__ == Bullet:
                    if obj.dy < 0:
                        caption += f"Player {cls} {c} position: (x={obj.center[0]}, y={obj.center[1]}) \n"
                    elif obj.dy > 0:
                        caption += f"Enemy {cls} {c} position: (x={obj.center[0]}, y={obj.center[1]}) \n"
                else:
                    caption += f"{cls} {c} position: (x={obj.center[0]}, y={obj.center[1]}) \n"
                c += 1
                
    caption = add_aliens_with_counts(caption, aliens)
    return caption

def add_aliens_as_ranges(caption, aliens):
    c = 0
    for alien in aliens:
        caption += f"Alien {c} position: (x={alien.center[0]}, y={alien.center[1]}) \n"
        c += 1
    return caption

def add_grouped_aliens_by_rows(caption, aliens):
    rows = {}
    for alien in aliens:
        y = alien.center[1]
        if y not in rows:
            rows[y] = []
        rows[y].append(alien.center[0])
    
    for y, x_values in sorted(rows.items()):
        x_values = sorted(x_values)
        caption += f"Row y={y}: x={x_values} \n"
    return caption

def add_aliens_as_ranges(caption, aliens):
    rows = {}
    for alien in aliens:
        y = alien.center[1]
        if y not in rows:
            rows[y] = []
        rows[y].append(alien.center[0])
    
    for y, x_values in sorted(rows.items()):
        x_values = sorted(x_values)
        x_min, x_max = min(x_values), max(x_values)
        step = x_values[1] - x_values[0] if len(x_values) > 1 else "N/A"
        caption += f"Row y={y}: x range=({x_min}, {x_max}), step={step} \n"
    return caption

def add_aliens_with_counts(caption, aliens):
    rows = {}
    for alien in aliens:
        y = alien.center[1]
        if y not in rows:
            rows[y] = []
        rows[y].append(alien.center[0])
    
    for y, x_values in sorted(rows.items()):
        count = len(x_values)
        x_values = sorted(x_values)
        caption += f"y={y}: {count} aliens at x={x_values} \n"
    return caption

def add_aliens_with_deltas(caption, aliens, previous_positions=None):
    if previous_positions is None:
        previous_positions = {i: alien.center for i, alien in enumerate(aliens)}

    current_positions = {i: alien.center for i, alien in enumerate(aliens)}
    for i, center in current_positions.items():
        if i in previous_positions:
            delta_x = center[0] - previous_positions[i][0]
            delta_y = center[1] - previous_positions[i][1]
            caption += f"Alien {i} movement: Δx={delta_x}, Δy={delta_y} \n"
        else:
            caption += f"Alien {i} position: (x={center[0]}, y={center[1]}) \n"
    return caption

