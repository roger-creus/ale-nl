from ocatari.ram.adventure import Player, YellowDragon, GreenDragon, RedDragon, BlackBat, DragonSword, YellowKey, BlackKey, WhiteKey, Magnet, BridgeEdge, Gate, Chalice

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Adventure game state.

    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, YellowDragon, GreenDragon, RedDragon, BlackBat,
              DragonSword, YellowKey, BlackKey, WhiteKey, Magnet, BridgeEdge, Gate, Chalice.

    Returns:
        A string containing a structured description of the game state.
    """
    # Define the expected object types.
    object_types = (
        Player, YellowDragon, GreenDragon, RedDragon, BlackBat,
        DragonSword, YellowKey, BlackKey, WhiteKey, Magnet, BridgeEdge, Gate, Chalice
    )

    # Group objects by their class name.
    objects_by_type = {
        cls.__name__: [obj for obj in objs if isinstance(obj, cls)]
        for cls in object_types
    }

    # For all objects, sort them by vertical (y) then horizontal (x) position using _xy.
    for type_name, obj_list in objects_by_type.items():
        obj_list.sort(key=lambda o: (o._xy[1], o._xy[0]))

    lines = []

    # --- Game Objects ---
    if objects_by_type.get("Player"):
        player_obj = objects_by_type["Player"][0]
        lines.append(f"Player Position: x={player_obj._xy[0]}, y={player_obj._xy[1]}")

    if objects_by_type.get("YellowDragon"):
        for i, dragon in enumerate(objects_by_type["YellowDragon"]):
            lines.append(f"Yellow Dragon {i+1} Position: x={dragon._xy[0]}, y={dragon._xy[1]}")

    if objects_by_type.get("GreenDragon"):
        for i, dragon in enumerate(objects_by_type["GreenDragon"]):
            lines.append(f"Green Dragon {i+1} Position: x={dragon._xy[0]}, y={dragon._xy[1]}")

    if objects_by_type.get("RedDragon"):
        for i, dragon in enumerate(objects_by_type["RedDragon"]):
            lines.append(f"Red Dragon {i+1} Position: x={dragon._xy[0]}, y={dragon._xy[1]}")

    if objects_by_type.get("BlackBat"):
        for i, bat in enumerate(objects_by_type["BlackBat"]):
            lines.append(f"Black Bat {i+1} Position: x={bat._xy[0]}, y={bat._xy[1]}")

    if objects_by_type.get("DragonSword"):
        for i, sword in enumerate(objects_by_type["DragonSword"]):
            lines.append(f"Dragon Sword {i+1} Position: x={sword._xy[0]}, y={sword._xy[1]}")

    if objects_by_type.get("YellowKey"):
        for i, key in enumerate(objects_by_type["YellowKey"]):
            lines.append(f"Yellow Key {i+1} Position: x={key._xy[0]}, y={key._xy[1]}")

    if objects_by_type.get("BlackKey"):
        for i, key in enumerate(objects_by_type["BlackKey"]):
            lines.append(f"Black Key {i+1} Position: x={key._xy[0]}, y={key._xy[1]}")

    if objects_by_type.get("WhiteKey"):
        for i, key in enumerate(objects_by_type["WhiteKey"]):
            lines.append(f"White Key {i+1} Position: x={key._xy[0]}, y={key._xy[1]}")

    if objects_by_type.get("Magnet"):
        for i, magnet in enumerate(objects_by_type["Magnet"]):
            lines.append(f"Magnet {i+1} Position: x={magnet._xy[0]}, y={magnet._xy[1]}")

    if objects_by_type.get("BridgeEdge"):
        for i, bridge in enumerate(objects_by_type["BridgeEdge"]):
            lines.append(f"Bridge Edge {i+1} Position: x={bridge._xy[0]}, y={bridge._xy[1]}")

    if objects_by_type.get("Gate"):
        for i, gate in enumerate(objects_by_type["Gate"]):
            lines.append(f"Gate {i+1} Position: x={gate._xy[0]}, y={gate._xy[1]}")

    if objects_by_type.get("Chalice"):
        for i, chalice in enumerate(objects_by_type["Chalice"]):
            lines.append(f"Chalice {i+1} Position: x={chalice._xy[0]}, y={chalice._xy[1]}")

    return "\n".join(lines)
