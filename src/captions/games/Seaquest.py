from ocatari.ram.seaquest import Player, Diver, Shark, Submarine, SurfaceSubmarine, EnemyMissile, PlayerMissile, PlayerScore, Lives, OxygenBar, OxygenBarDepleted, CollectedDiver

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Seaquest game state.

    Parameters:
        ram: The game RAM/state information (unused here, but available for future details).
        objs: A list of game objects which may include instances of:
              Player, Diver, Shark, Submarine, SurfaceSubmarine, EnemyMissile,
              PlayerMissile, PlayerScore, Lives, OxygenBar, OxygenBarDepleted, CollectedDiver.

    Returns:
        A string containing a structured description of the game state.
    """
    object_types = (
        Player, Diver, Shark, Submarine, SurfaceSubmarine,
        EnemyMissile, PlayerMissile, PlayerScore, Lives,
        OxygenBar, OxygenBarDepleted, CollectedDiver
    )

    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    hud_types = {"PlayerScore", "Lives", "OxygenBar", "OxygenBarDepleted", "CollectedDiver"}

    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- HUD Elements ---
    if objects_by_type.get("PlayerScore"):
        score_obj = objects_by_type["PlayerScore"][0]
        lines.append(f"Score: {score_obj.value}")

    if objects_by_type.get("Lives"):
        lives_obj = objects_by_type["Lives"][0]
        lines.append(f"Lives Remaining: {lives_obj.value}")

    if objects_by_type.get("OxygenBar"):
        oxygen_obj = objects_by_type["OxygenBar"][0]
        lines.append(f"Oxygen Level: {oxygen_obj.value}")

    if objects_by_type.get("CollectedDiver"):
        collected_diver_count = len(objects_by_type["CollectedDiver"])
        lines.append(f"Collected Divers: {collected_diver_count}")

    # --- Game Objects ---
    if objects_by_type.get("Player"):
        player_obj = objects_by_type["Player"][0]
        lines.append(f"Player Submarine Position: x={player_obj.center[0]}, y={player_obj.center[1]}")

    if objects_by_type.get("Diver"):
        for i, diver in enumerate(objects_by_type["Diver"]):
            lines.append(f"Diver {i+1} Position: x={diver.center[0]}, y={diver.center[1]}")

    if objects_by_type.get("Shark"):
        for i, shark in enumerate(objects_by_type["Shark"]):
            lines.append(f"Shark {i+1} Position: x={shark.center[0]}, y={shark.center[1]}")

    if objects_by_type.get("Submarine"):
        for i, sub in enumerate(objects_by_type["Submarine"]):
            lines.append(f"Enemy Submarine {i+1} Position: x={sub.center[0]}, y={sub.center[1]}")

    if objects_by_type.get("SurfaceSubmarine"):
        for i, sub in enumerate(objects_by_type["SurfaceSubmarine"]):
            lines.append(f"Surface Submarine {i+1} Position: x={sub.center[0]}, y={sub.center[1]}")

    if objects_by_type.get("EnemyMissile"):
        for i, missile in enumerate(objects_by_type["EnemyMissile"]):
            lines.append(f"Enemy Missile {i+1} Position: x={missile.center[0]}, y={missile.center[1]}")

    if objects_by_type.get("PlayerMissile"):
        for i, missile in enumerate(objects_by_type["PlayerMissile"]):
            lines.append(f"Player Torpedo {i+1} Position: x={missile.center[0]}, y={missile.center[1]}")

    return "\n".join(lines)
