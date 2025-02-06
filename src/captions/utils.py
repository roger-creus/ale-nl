from src.captions.games.SpaceInvaders import make_caption as make_caption_spaceinvaders
from src.captions.games.Freeway import make_caption as make_caption_freeway

ENVS_AVAILABLE = [
    "SpaceInvadersNoFrameskip-v4",
    "FreewayNoFrameskip-v4",
]

def clean_caption(caption):
    caption =  "\n".join([line.strip() for line in caption.split("\n")])
    caption = "\n".join([line for line in caption.split("\n") if line])
    return caption

def parse_caption(ram, objs, env_id):
    if "SpaceInvaders" in env_id:
        caption = make_caption_spaceinvaders(ram, objs)
    elif "Freeway" in env_id:
        caption = make_caption_freeway(ram, objs)
    else:
        raise NotImplementedError(f"Environment {env_id} not supported.")
    
    return clean_caption(caption)
    
