import gymnasium as gym
from IPython import embed
from nlp.caption_utils import parse_caption, ENVS_AVAIL

class AtariNLPWrapper(gym.Wrapper):
    """
    Wrapper for Atari environments to provide NLP observations. RAM annotations taken from:
    https://github.com/mila-iqia/atari-representation-learning/blob/master/atariari/benchmark/ram_annotations.py
    """
    def __init__(self, env, env_id):
        super().__init__(env)
        assert env_id in ENVS_AVAIL
        
        self.env = env
        self.env_id = env_id

    def reset(self):
        obs, info = self.env.reset()

        ram = self.env.ale.getRAM()
        caption = self.get_caption(ram)
        info['caption'] = caption
        return obs, info

    def step(self, action):
        obs, reward, term, trunc, info = self.env.step(action)
        
        ram = self.env.ale.getRAM()
        caption = self.get_caption(ram)
        info['caption'] = caption
        return obs, reward, term, trunc, info
    
    def get_caption(self, ram):
        return parse_caption(ram, self.env_id)