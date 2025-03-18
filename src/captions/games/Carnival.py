from ocatari.ram.carnival import Player, PlayerMissile, Owl, Duck, FlyingDuck, Rabbit, ExtraBullets, PlayerScore, AmmoBar, BonusSign, BonusValue, Wheel

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Carnival game state.
    
    For HUD elements (e.g. PlayerScore, BonusSign, BonusValue), if a meaningful value is available (via a 'value' attribute),
    output that value; otherwise, skip them.
    
    For non-HUD objects (Player, PlayerMissile, Owl, Duck, FlyingDuck, Rabbit, ExtraBullets, Wheel), output each instance's position.
    
    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, PlayerMissile, Owl, Duck, FlyingDuck, Rabbit, ExtraBullets,
              PlayerScore, AmmoBar, BonusSign, BonusValue, Wheel.
              
    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (
        Player, PlayerMissile, Owl, Duck, FlyingDuck, Rabbit, ExtraBullets,
        PlayerScore, AmmoBar, BonusSign, BonusValue, Wheel
    )
    
    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }
    
    # Define which HUD elements we consider.
    hud_types = {"PlayerScore", "AmmoBar", "BonusSign", "BonusValue"}
    
    # Helper to get an object's position.
    def get_xy(obj):
        if hasattr(obj, "_xy"):
            return obj._xy
        elif hasattr(obj, "xy"):
            return obj.xy
        else:
            return (None, None)
    
    # For non-HUD objects, sort by vertical (y) then horizontal (x) position.
    for type_name, obj_list in objects_by_type.items():
        if type_name not in hud_types:
            obj_list.sort(key=lambda o: (get_xy(o)[1] if get_xy(o)[1] is not None else 0,
                                         get_xy(o)[0] if get_xy(o)[0] is not None else 0))
    
    lines = []
    
    # --- HUD Elements ---
    # For each HUD element, if it has a meaningful value, output it.
    for hud in ["PlayerScore", "BonusSign", "BonusValue"]:
        if hud in objects_by_type and objects_by_type[hud]:
            hud_obj = objects_by_type[hud][0]
            if hasattr(hud_obj, "value"):
                lines.append(f"{hud}: {hud_obj.value}")
            # Otherwise, skip this HUD element.
    # (AmmoBar is skipped unless it provides a value)
    
    # --- Game Objects ---
    for type_name in ["Player", "PlayerMissile", "Owl", "Duck", "FlyingDuck", "Rabbit", "ExtraBullets", "Wheel"]:
        obj_list = objects_by_type.get(type_name, [])
        for i, obj in enumerate(obj_list):
            pos = get_xy(obj)
            if len(obj_list) == 1:
                lines.append(f"{type_name} Position: x={pos[0]}, y={pos[1]}")
            else:
                lines.append(f"{type_name} {i+1} Position: x={pos[0]}, y={pos[1]}")
    
    return "\n".join(lines)
