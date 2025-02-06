from ocatari.ram.game_objects import NoObject
from ocatari.ram.spaceinvaders import Player, Alien, Satellite, Shield, Bullet
from IPython import embed

def make_caption(ram, objs):
    ram_mappings = {
        "invaders_left_count": 17,
        "num_lives": 73,
    }
    
    lines = []
    lines.append(f"You have {ram[ram_mappings['num_lives']]} lives remaining.")
    lines.append(f"There are {ram[ram_mappings['invaders_left_count']]} aliens left on the screen.")
    
    object_types = (Player, Alien, Satellite, Shield, Bullet)
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }
    
    for type_name, obj_list in objects_by_type.items():
        obj_list.sort(key=lambda obj: (obj.center[1], obj.center[0]))
    
    aliens = objects_by_type.pop("Alien", [])
    for type_name, obj_list in objects_by_type.items():
        if obj_list:
            for index, obj in enumerate(obj_list):
                if type_name == "Bullet":
                    if hasattr(obj, "dy"):
                        if obj.dy < 0:
                            source = "player's"
                        elif obj.dy > 0:
                            source = "enemy's"
                        else:
                            source = "unknown"
                    else:
                        source = "unknown"
                    lines.append(
                        f"A {source} bullet (Bullet {index}) is at position (x={obj.center[0]}, y={obj.center[1]})."
                    )
                else:
                    lines.append(
                        f"{type_name} {index} is at position (x={obj.center[0]}, y={obj.center[1]})."
                    )
    
    lines.extend(describe_alien_rows(aliens))
    return "\n".join(lines)


def describe_alien_rows(aliens):
    if not aliens:
        return ["There are no aliens on the screen."]
    
    rows = {}
    for alien in aliens:
        y = alien.center[1]
        rows.setdefault(y, []).append(alien.center[0])
    
    descriptions = []
    for y in sorted(rows):
        x_positions = sorted(rows[y])
        count = len(x_positions)
        pos_list = ", ".join(str(x) for x in x_positions)
        descriptions.append(
            f"In row with y = {y}, there {'is' if count == 1 else 'are'} {count} alien{'s' if count != 1 else ''} at x positions: {pos_list}."
        )
    return descriptions