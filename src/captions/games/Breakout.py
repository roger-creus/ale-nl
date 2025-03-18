from ocatari.ram.breakout import Player, Ball, Block

def describe_block_rows(blocks):
    """
    Group blocks by their y-coordinate and generate a compact description.
    
    Parameters:
        blocks: A list of Block objects. Each Block has an attribute 'xy'.
        
    Returns:
        A list of strings, each describing one row of blocks.
    """
    if not blocks:
        return ["There are no blocks on the screen."]
    
    rows = {}
    for block in blocks:
        y = block.xy[1]
        rows.setdefault(y, []).append(block.xy[0])
    
    descriptions = []
    for y in sorted(rows):
        x_positions = sorted(rows[y])
        count = len(x_positions)
        pos_list = ", ".join(str(x) for x in x_positions)
        descriptions.append(
            f"In row with y = {y}, there {'is' if count == 1 else 'are'} {count} block{'s' if count != 1 else ''} at x positions: {pos_list}."
        )
    return descriptions


def make_caption(ram, objs):
    """
    Generate a structured caption for the current Breakout game state,
    reporting the positions of the player (paddle), ball(s), and grouping
    the blocks by rows.
    
    Parameters:
        ram: The game RAM/state information (unused here).
        objs: A list of game objects which may include instances of:
              Player, Ball, PlayerScore, Live, and Block.
              
    Returns:
        A string containing a structured description of the game state.
    """
    # Group objects by type.
    players = [obj for obj in objs if isinstance(obj, Player)]
    balls = [obj for obj in objs if isinstance(obj, Ball)]
    blocks = [obj for obj in objs if isinstance(obj, Block)]
    
    lines = []
    
    # Report the player (paddle) position.
    if players:
        p = players[0]
        lines.append(f"Player Position: x={p._xy[0]}, y={p._xy[1]}")
    
    # Report each ball's position.
    if balls:
        for i, ball in enumerate(balls):
            lines.append(f"Ball {i+1} Position: x={ball._xy[0]}, y={ball._xy[1]}")
    
    # Group blocks into rows and add the compact description.
    if blocks:
        block_descriptions = describe_block_rows(blocks)
        lines.extend(block_descriptions)
    
    return "\n".join(lines)