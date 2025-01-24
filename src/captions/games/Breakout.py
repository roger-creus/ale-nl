

def make_caption(ram):
    mappings = dict(
        ball_x=99,
        ball_y=101,
        player_x=72,
        blocks_hit_count=77,
        block_bit_map=range(30),  # see breakout bitmaps tab
        score=84# 5 for each hit
    )
    
    caption = f"""
        Score: {ram[mappings['score']]} \n
        Player position: x={ram[mappings['player_x']]} \n
        Ball position: (x={ram[mappings['ball_x']]}, y={ram[mappings['ball_y']]}) \n
        Blocks hit: {ram[mappings['blocks_hit_count']]} \n
        """
    return caption