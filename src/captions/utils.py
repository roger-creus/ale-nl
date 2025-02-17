from src.captions.games.SpaceInvaders import make_caption as make_caption_spaceinvaders
from src.captions.games.Freeway import make_caption as make_caption_freeway
from src.captions.games.Seaquest import make_caption as make_caption_seaquest
from src.captions.games.MsPacman import make_caption as make_caption_mspacman
from src.captions.games.Asterix import make_caption as make_caption_asterix
from src.captions.games.Adventure import make_caption as make_caption_adventure

ENVS_AVAILABLE = [
    "SpaceInvadersNoFrameskip-v4",
    "FreewayNoFrameskip-v4",
    "SeaquestNoFrameskip-v4",
    "MsPacmanNoFrameskip-v4",
    "AsterixNoFrameskip-v4",
    "AdventureNoFrameskip-v4",
]

def parse_caption(ram, objs, env_id):
    if "SpaceInvaders" in env_id:
        caption = make_caption_spaceinvaders(ram, objs)
    elif "Freeway" in env_id:
        caption = make_caption_freeway(ram, objs)
    elif "Seaquest" in env_id:
        caption = make_caption_seaquest(ram, objs)
    elif "MsPacman" in env_id:
        caption = make_caption_mspacman(ram, objs)
    elif "Asterix" in env_id:
        caption = make_caption_asterix(ram, objs)
    elif "Adventure" in env_id:
        caption = make_caption_adventure(ram, objs)
    else:
        raise NotImplementedError(f"Environment {env_id} not supported.")
    
    return caption
    
