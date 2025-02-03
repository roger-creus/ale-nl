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

############ ASCII Map ############
def make_ascii_map(ram, objs, width=20, height=10):
    ram_mappings = dict(
        invaders_left_count=17,
        num_lives=73,
    )
    
    # Initialize empty grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Object information
    clsses = {Player, Alien, Satellite, Shield, Bullet}
    objs = {cls.__name__ : [obj for obj in objs if obj.__class__ == cls] for cls in clsses}
    
    # Sort objects by coordinates
    for cls, o in objs.items():
        objs[cls] = sorted(o, key=lambda x: (x.center[1], x.center[0]))
    
    # Map objects to ASCII symbols
    symbols = {
        'Player': 'P',
        'Alien': 'A',
        'Satellite': 'S',
        'Shield': '#',
        'Bullet': '|',
    }
    
    # Populate grid with objects
    for cls, o in objs.items():
        for obj in o:
            x, y = obj.center[0] * width // 160, obj.center[1] * height // 210  # Normalize coordinates
            x, y = int(min(width - 1, x)), int(min(height - 1, y))  # Keep within bounds
            if cls == 'Bullet':
                grid[y][x] = '!' if obj.dy < 0 else 'i'  # Different symbols for player/enemy bullets
            else:
                grid[y][x] = symbols[cls]
    
    # Convert grid to ASCII representation
    ascii_map = "\n".join("".join(row) for row in grid)
    
    # Add game info
    caption = f"Lives: {ram[ram_mappings['num_lives']]}  Aliens Left: {ram[ram_mappings['invaders_left_count']]}\n"
    caption += ascii_map
    return caption
