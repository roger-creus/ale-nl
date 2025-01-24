from src.captions.games.SpaceInvaders import make_caption as make_caption_spaceinvaders
from src.captions.games.MsPacman import make_caption as make_caption_mspacman
from src.captions.games.Breakout import make_caption as make_caption_breakout

ENVS_AVAILABLE = [
    "SpaceInvadersNoFrameskip-v4",
    "MsPacmanNoFrameskip-v4",
    "BreakoutNoFrameskip-v4",
]

def clean_caption(caption):
    caption =  "\n".join([line.strip() for line in caption.split("\n")])
    caption = "\n".join([line for line in caption.split("\n") if line])
    return caption

def parse_caption(ram, objs, env_id):
    if "SpaceInvaders" in env_id:
        caption = make_caption_spaceinvaders(ram, objs)
    elif "MsPacman" in env_id:
        caption = make_caption_mspacman(ram, objs)
    elif "Breakout" in env_id:
        caption = make_caption_breakout(ram, objs)
    else:
        raise NotImplementedError(f"Environment {env_id} not supported.")
    
    return clean_caption(caption)
    
