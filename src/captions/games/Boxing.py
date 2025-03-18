from ocatari.ram.boxing import Player, Enemy, Clock, PlayerScore, EnemyScore

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Boxing game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Enemy, Clock, PlayerScore, EnemyScore.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define expected object types.
    object_types = (Player, Enemy, Clock, PlayerScore, EnemyScore)

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    lines = []

    # --- In-Game Objects (Player & Enemy) ---
    if objects_by_type.get("Player"):
        player = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player._xy[0]}, y={player._xy[1]}")
        lines.append(f"Player Right Arm Length: {player.right_arm_length}")
        lines.append(f"Player Left Arm Length: {player.left_arm_length}")

    if objects_by_type.get("Enemy"):
        enemy = objects_by_type["Enemy"][0]
        lines.append(f"Enemy Position: x={enemy._xy[0]}, y={enemy._xy[1]}")
        lines.append(f"Enemy Right Arm Length: {enemy.right_arm_length}")
        lines.append(f"Enemy Left Arm Length: {enemy.left_arm_length}")

    return "\n".join(lines)
