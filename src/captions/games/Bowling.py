from ocatari.ram.bowling import Player, Ball, Pin, PlayerScore, PlayerRound, Player2Round

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Bowling game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Ball, Pin, PlayerScore, PlayerRound, Player2Round.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (Player, Ball, Pin, PlayerScore, PlayerRound, Player2Round)

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    # HUD elements (their positions are not spatially sorted)
    hud_types = {"PlayerScore", "PlayerRound", "Player2Round"}

    # For non-HUD objects, sort by vertical (y) then horizontal (x) using center.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- In-Game Objects ---
    if objects_by_type.get("Player"):
        player_obj = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player_obj.center[0]}, y={player_obj.center[1]}")
    
    if objects_by_type.get("Ball"):
        for i, ball in enumerate(objects_by_type["Ball"]):
            if len(objects_by_type["Ball"]) == 1:
                lines.append(f"Ball Position: x={ball.center[0]}, y={ball.center[1]}")
            else:
                lines.append(f"Ball {i+1} Position: x={ball.center[0]}, y={ball.center[1]}")
    
    if objects_by_type.get("Pin"):
        for i, pin in enumerate(objects_by_type["Pin"]):
            lines.append(f"Pin {i+1} Position: x={pin.center[0]}, y={pin.center[1]}")

    return "\n".join(lines)
