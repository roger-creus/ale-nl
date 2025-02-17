from ocatari.ram.beamrider import Player, Player_Projectile, Torpedos, Saucer, Rejuvenator, Sentinel, Blocker, Jumper, Charger, Bouncecraft, Chriper, Rock, Torpedos_Available, Enemy_Projectile, HUD, Enemy_Amount, Life

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Beamrider game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Player_Projectile, Torpedos, Saucer, Rejuvenator,
              Sentinel, Blocker, Jumper, Charger, Bouncecraft, Chriper,
              Rock, Torpedos_Available, Enemy_Projectile, HUD, Enemy_Amount, Life.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (
        Player, Player_Projectile, Torpedos, Saucer, Rejuvenator,
        Sentinel, Blocker, Jumper, Charger, Bouncecraft, Chriper,
        Rock, Torpedos_Available, Enemy_Projectile, HUD, Enemy_Amount, Life
    )

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    # Define HUD types. These objects will not be spatially sorted.
    hud_types = {"Torpedos_Available", "HUD", "Enemy_Amount", "Life"}

    # For non-HUD objects, sort by vertical (y) then horizontal (x) using _xy.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (o.center[1], o.center[0]))

    lines = []

    # --- HUD Elements ---
    if objects_by_type.get("Life"):
        lives_count = len(objects_by_type["Life"])
        lines.append(f"Lives: {lives_count}")
    
    if objects_by_type.get("Torpedos_Available"):
        ta_obj = objects_by_type["Torpedos_Available"][0]
        lines.append(f"Torpedos Available Position: x={ta_obj.center[0]}, y={ta_obj.center[1]}")
    
    if objects_by_type.get("Enemy_Amount"):
        ea_obj = objects_by_type["Enemy_Amount"][0]
        lines.append(f"Enemy Amount Position: x={ea_obj.center[0]}, y={ea_obj.center[1]}")
    
    if objects_by_type.get("HUD"):
        hud_obj = objects_by_type["HUD"][0]
        lines.append(f"HUD Position: x={hud_obj.center[0]}, y={hud_obj.center[1]}")

    # --- Game Objects ---
    if objects_by_type.get("Player"):
        player = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player.center[0]}, y={player.center[1]}")
    
    if objects_by_type.get("Player_Projectile"):
        for i, proj in enumerate(objects_by_type["Player_Projectile"]):
            lines.append(f"Player Projectile {i+1} Position: x={proj.center[0]}, y={proj.center[1]}")
    
    if objects_by_type.get("Torpedos"):
        for i, torp in enumerate(objects_by_type["Torpedos"]):
            lines.append(f"Torpedo {i+1} Position: x={torp.center[0]}, y={torp.center[1]}")
    
    if objects_by_type.get("Saucer"):
        for i, saucer in enumerate(objects_by_type["Saucer"]):
            lines.append(f"Saucer {i+1} Position: x={saucer.center[0]}, y={saucer.center[1]}")
    
    if objects_by_type.get("Rejuvenator"):
        for i, rejuvenator in enumerate(objects_by_type["Rejuvenator"]):
            lines.append(f"Rejuvenator {i+1} Position: x={rejuvenator.center[0]}, y={rejuvenator.center[1]}")
    
    if objects_by_type.get("Sentinel"):
        for i, sentinel in enumerate(objects_by_type["Sentinel"]):
            lines.append(f"Sentinel {i+1} Position: x={sentinel.center[0]}, y={sentinel.center[1]}")
    
    if objects_by_type.get("Blocker"):
        for i, blocker in enumerate(objects_by_type["Blocker"]):
            lines.append(f"Blocker {i+1} Position: x={blocker.center[0]}, y={blocker.center[1]}")
    
    if objects_by_type.get("Jumper"):
        for i, jumper in enumerate(objects_by_type["Jumper"]):
            lines.append(f"Jumper {i+1} Position: x={jumper.center[0]}, y={jumper.center[1]}")
    
    if objects_by_type.get("Charger"):
        for i, charger in enumerate(objects_by_type["Charger"]):
            lines.append(f"Charger {i+1} Position: x={charger.center[0]}, y={charger.center[1]}")
    
    if objects_by_type.get("Bouncecraft"):
        for i, bounce in enumerate(objects_by_type["Bouncecraft"]):
            lines.append(f"Bouncecraft {i+1} Position: x={bounce.center[0]}, y={bounce.center[1]}")
    
    if objects_by_type.get("Chriper"):
        for i, chirper in enumerate(objects_by_type["Chriper"]):
            lines.append(f"Chriper {i+1} Position: x={chirper.center[0]}, y={chirper.center[1]}")
    
    if objects_by_type.get("Rock"):
        for i, rock in enumerate(objects_by_type["Rock"]):
            lines.append(f"Rock {i+1} Position: x={rock.center[0]}, y={rock.center[1]}")
    
    if objects_by_type.get("Enemy_Projectile"):
        for i, eproj in enumerate(objects_by_type["Enemy_Projectile"]):
            lines.append(f"Enemy Projectile {i+1} Position: x={eproj.center[0]}, y={eproj.center[1]}")
    
    return "\n".join(lines)
