from ocatari.ram.battlezone import Player, Crosshair, Shot, Radar, Radar_Content, Blue_Tank, Yellow_Blue_Tank, Red_Thing, Boss, Score, Life

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Battlezone game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Crosshair, Shot, Radar, Radar_Content, Blue_Tank,
              Yellow_Blue_Tank, Red_Thing, Boss, Score, Life.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (
        Player, Crosshair, Shot, Radar, Radar_Content,
        Blue_Tank, Yellow_Blue_Tank, Red_Thing, Boss, Score, Life
    )

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    # Treat Score and Life as HUD elements.
    hud_types = {"Score", "Life"}

    # For non-HUD objects, sort by vertical (y) then horizontal (x) using _xy.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- HUD Elements ---
    if objects_by_type.get("Score"):
        score_obj = objects_by_type["Score"][0]
        # Use 'score' attribute as defined in the Score class.
        lines.append(f"Score: {score_obj.score}")
    if objects_by_type.get("Life"):
        # Assuming each Life object represents one remaining life.
        lives_count = len(objects_by_type["Life"])
        lines.append(f"Lives: {lives_count}")

    # --- Game Objects ---
    if objects_by_type.get("Player"):
        player_obj = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player_obj.center[0]}, y={player_obj.center[1]}")
    
    if objects_by_type.get("Crosshair"):
        for i, crosshair in enumerate(objects_by_type["Crosshair"]):
            lines.append(f"Crosshair {i+1} Position: x={crosshair.center[0]}, y={crosshair.center[1]}")
    
    if objects_by_type.get("Shot"):
        for i, shot in enumerate(objects_by_type["Shot"]):
            lines.append(f"Shot {i+1} Position: x={shot.center[0]}, y={shot.center[1]}")
    
    if objects_by_type.get("Radar_Content"):
        for i, rc in enumerate(objects_by_type["Radar_Content"]):
            lines.append(f"Radar Content {i+1} Position: x={rc.center[0]}, y={rc.center[1]}")
    
    if objects_by_type.get("Blue_Tank"):
        for i, tank in enumerate(objects_by_type["Blue_Tank"]):
            lines.append(f"Blue Tank {i+1} Position: x={tank.center[0]}, y={tank.center[1]}")
    
    if objects_by_type.get("Yellow_Blue_Tank"):
        for i, tank in enumerate(objects_by_type["Yellow_Blue_Tank"]):
            lines.append(f"Yellow-Blue Tank {i+1} Position: x={tank.center[0]}, y={tank.center[1]}")
    
    if objects_by_type.get("Red_Thing"):
        for i, rt in enumerate(objects_by_type["Red_Thing"]):
            lines.append(f"Red Thing {i+1} Position: x={rt.center[0]}, y={rt.center[1]}")
    
    if objects_by_type.get("Boss"):
        for i, boss in enumerate(objects_by_type["Boss"]):
            lines.append(f"Boss {i+1} Position: x={boss.center[0]}, y={boss.center[1]}")
    
    return "\n".join(lines)
