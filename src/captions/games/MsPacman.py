DIRECTIONS = {
    0: "UP",
    1: "RIGHT",
    2: "DOWN",
    3: "LEFT"
}

def make_caption(ram):
    mappings = dict(
        enemy_sue_x=6,
        enemy_inky_x=7,
        enemy_pinky_x=8,
        enemy_blinky_x=9,
        enemy_sue_y=12,
        enemy_inky_y=13,
        enemy_pinky_y=14,
        enemy_blinky_y=15,
        player_x=10,
        player_y=16,
        fruit_x=11,
        fruit_y=17,
        ghosts_count=19,
        player_direction=56,
        dots_eaten_count=119,
        player_score=120,
        num_lives=123
    )
    
    if ram[mappings["fruit_x"]] == 0 and ram[mappings["fruit_y"]] == 0:
        fruit_sentence = "No fruit on the map."
    else:
        fruit_sentence = f"Fruit position: (x={ram[mappings['fruit_x']]}, y={ram[mappings['fruit_y']]})"
    
    caption = f"""
            Ghosts left: {ram[mappings['ghosts_count']]} \n
            Lives: {ram[mappings['num_lives']]} \n
            Score: {ram[mappings['player_score']]} \n
            Player position: (x={ram[mappings['player_x']]}, y={ram[mappings['player_y']]}) \n
            Player direction: {DIRECTIONS[ram[mappings['player_direction']]]} \n
            Pellets eaten: {ram[mappings['dots_eaten_count']]} \n
            {fruit_sentence} \n
            Sue position: (x={ram[mappings['enemy_sue_x']]}, y={ram[mappings['enemy_sue_y']]}) \n
            Inky position: (x={ram[mappings['enemy_inky_x']]}, y={ram[mappings['enemy_inky_y']]}) \n
            Pinky position: (x={ram[mappings['enemy_pinky_x']]}, y={ram[mappings['enemy_pinky_y']]}) \n
            Blinky position: (x={ram[mappings['enemy_blinky_x']]}, y={ram[mappings['enemy_blinky_y']]}) \n
            """
            
    return caption