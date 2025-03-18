from ocatari.ram.kungfumaster import *

def make_caption(ram, objs):
    """
    Generate a structured caption for the current Kung-Fu Master game state.
    
    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Knife_Throwers, Henchmen, Snake, Dragon, Dragon_Smoke, Dragon_Balls,
              Red_Ball, Airball, Small_Enemy, Killer_Moth, Enemy_Final_Fighter, Knifes,
              Dragon_Fire, Score, Time, Lives, Player_Health_Bar, Enemy_Health_Bar.
              
    Returns:
        A string containing a structured description of the game state.
    """
    # Group objects by type.
    player = next((obj for obj in objs if isinstance(obj, Player)), None)
    knife_throwers = [obj for obj in objs if isinstance(obj, Knife_Throwers)]
    henchmen = [obj for obj in objs if isinstance(obj, Henchmen)]
    snakes = [obj for obj in objs if isinstance(obj, Snake)]
    dragons = [obj for obj in objs if isinstance(obj, Dragon)]
    dragon_smokes = [obj for obj in objs if isinstance(obj, Dragon_Smoke)]
    dragon_balls = [obj for obj in objs if isinstance(obj, Dragon_Balls)]
    red_balls = [obj for obj in objs if isinstance(obj, Red_Ball)]
    airballs = [obj for obj in objs if isinstance(obj, Airball)]
    small_enemies = [obj for obj in objs if isinstance(obj, Small_Enemy)]
    killer_moths = [obj for obj in objs if isinstance(obj, Killer_Moth)]
    final_fighters = [obj for obj in objs if isinstance(obj, Enemy_Final_Fighter)]
    knives = [obj for obj in objs if isinstance(obj, Knifes)]
    dragon_fires = [obj for obj in objs if isinstance(obj, Dragon_Fire)]
    
    score = next((obj for obj in objs if isinstance(obj, Score)), None)
    time = next((obj for obj in objs if isinstance(obj, Time)), None)
    lives = next((obj for obj in objs if isinstance(obj, Lives)), None)
    player_health = next((obj for obj in objs if isinstance(obj, Player_Health_Bar)), None)
    enemy_health = next((obj for obj in objs if isinstance(obj, Enemy_Health_Bar)), None)

    lines = []
    
    # --- HUD Elements ---
    if score and hasattr(score, "value"):
        lines.append(f"Score: {score.value}")
    if time and hasattr(time, "value"):
        lines.append(f"Time Left: {time.value}")
    if lives and hasattr(lives, "value"):
        lines.append(f"Lives Remaining: {lives.value}")
    if player_health:
        lines.append(f"Player Health: {player_health.wh[0]}")
    if enemy_health:
        lines.append(f"Enemy Health: {enemy_health.wh[0]}")

    # --- Player ---
    if player:
        lines.append(f"Player Position: x={player._xy[0]}, y={player._xy[1]}")

    # --- Enemies and Objects ---
    if knife_throwers:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in knife_throwers)
        lines.append(f"Knife Throwers at: {positions}")
    if henchmen:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in henchmen)
        lines.append(f"Henchmen at: {positions}")
    if snakes:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in snakes)
        lines.append(f"Snakes at: {positions}")
    if dragons:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in dragons)
        lines.append(f"Dragons at: {positions}")
    if dragon_smokes:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in dragon_smokes)
        lines.append(f"Dragon Smoke at: {positions}")
    if dragon_balls:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in dragon_balls)
        lines.append(f"Dragon Balls at: {positions}")
    if red_balls:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in red_balls)
        lines.append(f"Red Balls at: {positions}")
    if airballs:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in airballs)
        lines.append(f"Airballs at: {positions}")
    if small_enemies:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in small_enemies)
        lines.append(f"Small Enemies at: {positions}")
    if killer_moths:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in killer_moths)
        lines.append(f"Killer Moths at: {positions}")
    if final_fighters:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in final_fighters)
        lines.append(f"Final Fighters at: {positions}")
    if knives:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in knives)
        lines.append(f"Knives in Air at: {positions}")
    if dragon_fires:
        positions = ", ".join(f"(x={e._xy[0]}, y={e._xy[1]})" for e in dragon_fires)
        lines.append(f"Dragon Fire at: {positions}")

    return "\n".join(lines)
