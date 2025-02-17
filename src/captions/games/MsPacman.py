import math
from ocatari.ram.mspacman import Player, Ghost, Fruit, PowerPill, Pill, Score, Life

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Ms. Pac-Man game state.
    Now lists only the 10 closest pellets instead of clustering them.
    """
    object_types = (Player, Ghost, Fruit, PowerPill, Pill, Score, Life)
    
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }
    
    # HUD elements do not require spatial sorting.
    hud_types = {"Score", "Life"}
    
    # For non-HUD objects, sort by y then x.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- HUD Elements ---
    if objects_by_type.get("Score"):
        lines.append(f"Score: {objects_by_type['Score'][0].value}")
    if objects_by_type.get("Life"):
        lines.append(f"Lives Remaining: {objects_by_type['Life'][0].value}")

    # --- Player ---
    if objects_by_type.get("Player"):
        player = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player.center[0]}, y={player.center[1]}")
    else:
        player = None

    # --- Ghosts ---
    if objects_by_type.get("Ghost"):
        for i, ghost in enumerate(objects_by_type["Ghost"]):
            lines.append(f"Ghost {i+1} Position: x={ghost.center[0]}, y={ghost.center[1]}")

    # --- Fruit ---
    if objects_by_type.get("Fruit"):
        for i, fruit in enumerate(objects_by_type["Fruit"]):
            lines.append(f"Fruit {i+1} Position: x={fruit.center[0]}, y={fruit.center[1]}")

    # --- Power Pills ---
    if objects_by_type.get("PowerPill"):
        for i, pill in enumerate(objects_by_type["PowerPill"]):
            lines.append(f"Power Pill {i+1} Position: x={pill.center[0]}, y={pill.center[1]}")

    # --- Pellets (Top 10 Closest) ---
    if player and objects_by_type.get("Pill"):
        pills = objects_by_type["Pill"]
        pills.sort(key=lambda p: euclidean_distance(p._xy, player._xy))
        closest_pills = pills[:10]
        for i, pill in enumerate(closest_pills):
            lines.append(f"Closest Pellet {i+1} Position: x={pill.center[0]}, y={pill.center[1]}")

    return "\n".join(lines)


def euclidean_distance(p1, p2):
    """Compute the Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
