from ocatari.ram.asterix import Player, Enemy, Score, Lives, Consumable, Reward

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Asterix game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Enemy, Score, Lives, Consumable, Reward.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (Player, Enemy, Score, Lives, Consumable, Reward)

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    # HUD objects: Score and Lives (no spatial sorting required).
    hud_types = {"Score", "Lives"}

    # For non-HUD objects, sort them by vertical then horizontal position using _xy.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- HUD Elements ---
    if objects_by_type.get("Score"):
        score_obj = objects_by_type["Score"][0]
        lines.append(f"Score: {score_obj.value}")
    if objects_by_type.get("Lives"):
        # If more than one Lives object exists, we report the count.
        lives_count = len(objects_by_type["Lives"])
        lines.append(f"Lives: {lives_count}")

    # --- Game Objects ---
    # Player (Asterix)
    if objects_by_type.get("Player"):
        player_obj = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player_obj.center[0]}, y={player_obj.center[1]}")

    # Enemies (e.g., lyres or other harmful objects)
    if objects_by_type.get("Enemy"):
        for i, enemy in enumerate(objects_by_type["Enemy"]):
            lines.append(f"Enemy {i+1} Position: x={enemy.center[0]}, y={enemy.center[1]}")

    # Consumables (e.g., lyres that you should avoid or similar objects)
    if objects_by_type.get("Consumable"):
        for i, consumable in enumerate(objects_by_type["Consumable"]):
            lines.append(f"Consumable {i+1} Position: x={consumable.center[0]}, y={consumable.center[1]}")

    # Rewards (beneficial objects to collect)
    if objects_by_type.get("Reward"):
        for i, reward in enumerate(objects_by_type["Reward"]):
            lines.append(f"Reward {i+1} Position: x={reward.center[0]}, y={reward.center[1]}")

    return "\n".join(lines)
