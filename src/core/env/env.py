import gymnasium as gym
import numpy as np
from ocatari.core import OCAtari

from IPython import embed

class FireResetEnv(gym.Wrapper[np.ndarray, int, np.ndarray, int]):
    def __init__(self, env: gym.Env) -> None:
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space
        
        assert env.unwrapped.get_action_meanings()[1] == "FIRE" 
        assert len(env.unwrapped.get_action_meanings()) >= 3

    def reset(self, **kwargs):
        self.env.reset(**kwargs)
        obs, _, terminated, truncated, _ = self.env.step(1)
        if terminated or truncated:
            self.env.reset(**kwargs)
        obs, _, terminated, truncated, _ = self.env.step(2)
        if terminated or truncated:
            self.env.reset(**kwargs)
        return obs, {}
    
    @property
    def objects(self):
        return self.env.objects

class NoopResetEnv(gym.Wrapper[np.ndarray, int, np.ndarray, int]):
    def __init__(self, env: gym.Env, noop_max: int = 30) -> None:
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space
        self.noop_max = noop_max
        self.override_num_noops = None
        self.noop_action = 0
        assert env.unwrapped.get_action_meanings()[0] == "NOOP"

    def reset(self, **kwargs):
        self.env.reset(**kwargs)
        if self.override_num_noops is not None:
            noops = self.override_num_noops
        else:
            noops = self.unwrapped.np_random.integers(1, self.noop_max + 1)
        assert noops > 0
        obs = np.zeros(0)
        info: dict = {}
        for _ in range(noops):
            obs, _, terminated, truncated, info = self.env.step(self.noop_action)
            if terminated or truncated:
                obs, info = self.env.reset(**kwargs)
        return obs, info
    
    @property
    def objects(self):
        return self.env.objects

def make_env(args):
    env = OCAtari(args.env_id, mode="ram", hud=True, render_mode="rgb_array")
    env = NoopResetEnv(env, noop_max=30)
    if "FIRE" in env.unwrapped.get_action_meanings():
        env = FireResetEnv(env)
    env.action_space.seed(args.seed)
    env.observation_space.seed(args.seed)
    return env