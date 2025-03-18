from ocatari.ram.demonattack import Player, Enemy, EnemyPart, PlayerMissile, EnemyMissile, Score, Lives


def make_caption(ram, objs):
    """
    Generate a structured caption for the current Demon Attack game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Enemy, EnemyPart, PlayerMissile, EnemyMissile, Score, Lives.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (Player, Enemy, EnemyPart, PlayerMissile, EnemyMissile, Score, Lives)
    
    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }
    
    # Define HUD elements.
    hud_types = {"Score", "Lives"}
    
    # Helper function to get an object's position (using _xy).
    def get_xy(obj):
        return obj._xy if hasattr(obj, "_xy") else (None, None)
    
    # For non-HUD objects, sort by vertical (y) then horizontal (x) position.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (get_xy(o)[1] if get_xy(o)[1] is not None else 0,
                                         get_xy(o)[0] if get_xy(o)[0] is not None else 0))
    
    lines = []
    
    # --- HUD Elements ---
    # For Score and Lives, output the actual value if available.
    if objects_by_type.get("Score"):
        score_obj = objects_by_type["Score"][0]
        if hasattr(score_obj, "value"):
            lines.append(f"Score: {score_obj.value}")
    if objects_by_type.get("Lives"):
        lives_obj = objects_by_type["Lives"][0]
        if hasattr(lives_obj, "value"):
            lines.append(f"Lives: {lives_obj.value}")
    
    # --- Game Objects ---
    if objects_by_type.get("Player"):
        player = objects_by_type["Player"][0]
        pos = get_xy(player)
        lines.append(f"Player Position: x={pos[0]}, y={pos[1]}")
    
    if objects_by_type.get("Enemy"):
        for i, enemy in enumerate(objects_by_type["Enemy"]):
            pos = get_xy(enemy)
            lines.append(f"Enemy {i+1} Position: x={pos[0]}, y={pos[1]}")
    
    if objects_by_type.get("EnemyPart"):
        for i, part in enumerate(objects_by_type["EnemyPart"]):
            pos = get_xy(part)
            lines.append(f"Enemy Part {i+1} Position: x={pos[0]}, y={pos[1]}")
    
    if objects_by_type.get("PlayerMissile"):
        for i, missile in enumerate(objects_by_type["PlayerMissile"]):
            pos = get_xy(missile)
            lines.append(f"Player Missile {i+1} Position: x={pos[0]}, y={pos[1]}")
    
    if objects_by_type.get("EnemyMissile"):
        for i, missile in enumerate(objects_by_type["EnemyMissile"]):
            pos = get_xy(missile)
            lines.append(f"Enemy Missile {i+1} Position: x={pos[0]}, y={pos[1]}")
    
    return "\n".join(lines)
