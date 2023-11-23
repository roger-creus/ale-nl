ENVS_AVAIL = [
    "ALE/SpaceInvaders-v5",
    "ALE/MsPacman-v5",
]

def parse_caption(ram, env_id):
    def parse_space_invaders_caption(ram):
        mappings = dict(
            invaders_left_count=17,
            player_score=104,
            num_lives=73,
            player_x=28,
            enemies_x=26,
            missiles_y=9,
            enemies_y=24
        )
        caption = f"""
                    There are {ram[mappings['invaders_left_count']]} invaders left. \n
                    The player has {ram[mappings['num_lives']]} lives. \n
                    The player's score is {ram[mappings['player_score']]} points. \n
                    The player is at x position {ram[mappings['player_x']]}. \n
                    The player bullet's y position {ram[mappings['missiles_y']]}. \n
                    The enemies are at x position {ram[mappings['enemies_x']]} and y position {ram[mappings['enemies_y']]}.\n
                    """
        return caption
    
    def parse_mspacman_caption(ram):
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
        caption = f"""
                    There are {ram[mappings['ghosts_count']]} ghosts left. \n
                    The player has {ram[mappings['num_lives']]} lives. \n
                    The player's score is {ram[mappings['player_score']]} points. \n
                    The player is at x position {ram[mappings['player_x']]} and y position {ram[mappings['player_y']]}. \n
                    The player is facing {ram[mappings['player_direction']]}. \n
                    The player has eaten {ram[mappings['dots_eaten_count']]} dots. \n
                    The fruit is at x position {ram[mappings['fruit_x']]} and y position {ram[mappings['fruit_y']]}. \n
                    The Sue ghost is at x position {ram[mappings['enemy_sue_x']]} and y position {ram[mappings['enemy_sue_y']]}. \n
                    The Inky ghost is at x position {ram[mappings['enemy_inky_x']]} and y position {ram[mappings['enemy_inky_y']]}. \n
                    The Pinky ghost is at x position {ram[mappings['enemy_pinky_x']]} and y position {ram[mappings['enemy_pinky_y']]}. \n
                    The Blinky ghost is at x position {ram[mappings['enemy_blinky_x']]} and y position {ram[mappings['enemy_blinky_y']]}. \n
                    """
        return caption

    if "SpaceInvaders" in env_id:
        return parse_space_invaders_caption(ram)
    elif "MsPacman" in env_id:
        return parse_mspacman_caption(ram)
    else:
        raise NotImplementedError(f"Environment {env_id} not supported.")