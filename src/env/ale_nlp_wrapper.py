import gymnasium as gym
from collections import deque
from src.captions.utils import parse_caption, ENVS_AVAILABLE

from IPython import embed

class ALENLPWrapper(gym.Wrapper):
    def __init__(
        self,
        env,
        env_id,
        frame_skip=4,
        context_length=0,
    ):
        assert env_id in ENVS_AVAILABLE
        
        # env
        self.env = env
        self.action_meanings = {i: action for i, action in enumerate(self.env.unwrapped.get_action_meanings())}
        self.env_id = env_id
        self.frame_skip = frame_skip
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

        # nlp
        self.context_length = context_length

    def reset(self):
        obs, info = self.env.reset()
        ram = self.env.unwrapped.ale.getRAM()
        objs = self.env.objects
        current_caption = self.get_current_caption(ram, objs)
        self.init_prompt_context()
        info["caption"] = self.build_caption(self.prompt_context, current_caption)
        self.prompt_context["states"].append(current_caption)
        return obs, info

    def step(self, action):
        total_reward = 0.0
        term = False
        trunc = False
        skipped_captions = []
        final_info = None
        
        for _ in range(self.frame_skip):
            obs, reward, term, trunc, info = self.env.step(action)
            ram = self.env.unwrapped.ale.getRAM()
            objs = self.env.objects
            current_caption = self.get_current_caption(ram, objs)
            skipped_captions.append(current_caption)

            total_reward += reward
            if term or trunc:
                final_info = info
                break

        skipped_caption_summary = self.summarize_captions(skipped_captions)
        self.prompt_context["actions"].append(self.action_meanings[action])
        self.prompt_context["rewards"].append(total_reward)
        self.prompt_context["terminals"].append(term or trunc)
        
        aggregated_caption_summary = self.build_caption(self.prompt_context, skipped_caption_summary)
        self.prompt_context["states"].append(skipped_caption_summary)
        
        if term or trunc:
            if final_info is not None:
                final_info['caption'] = aggregated_caption_summary
            
            return obs, total_reward, term, trunc, final_info
        else:
            info['caption'] = aggregated_caption_summary
            return obs, total_reward, term, trunc, info

    def get_current_caption(self, ram, objs):
        return parse_caption(ram, objs, self.env_id)
    
    def build_caption(self, prompt_context, current_caption):
        """
        Builds the full caption prompt for the current timestep, including historical context.
        Starts from the oldest state and ends with the current state.
        """
        caption = ""
        first = True
        n = len(prompt_context['states']) + 1
        for i in range(n):      
            if not first:
                caption += f"\n-----------------\n"
                
            if first:
                first = False
                
            # current state
            if i == n-1:
                caption += f"<TIMESTEP>\nt (current)\n<\TIMESTEP>\n"
                caption += f"<STATE>\n{current_caption}\n<\STATE>"
                
            # history states
            else:
                caption += f"<TIMESTEP>\nt-{n-i+1}\n<\TIMESTEP>\n"
                caption += f"<STATE>\n{prompt_context['states'][i]}\n<\STATE>\n"
                caption += f"<ACTION>\n{prompt_context['actions'][i]}\n<\ACTION>\n"
                caption += f"<REWARD>\n{prompt_context['rewards'][i]}\n<\REWARD>\n"
                # caption += f"<TERMINAL>\n{prompt_context['terminals'][i]}\n<\TERMINAL>"
            
        return caption
        
    def init_prompt_context(self):
        self.prompt_context = {
            "states": deque(maxlen=self.context_length),
            "actions": deque(maxlen=self.context_length),
            "rewards": deque(maxlen=self.context_length),
            "terminals": deque(maxlen=self.context_length),
        }

    def summarize_captions(self, captions):
        if len(captions) == 1:
            return captions[0]

        parsed_captions = [self.parse_caption_to_dict(caption) for caption in captions]

        summary = {}
        for caption_dict in parsed_captions:
            for key, value in caption_dict.items():
                summary[key] = value  # Always overwrite to keep only the latest value

        summary_str = "\n".join(f"{key}: {value}" for key, value in summary.items())
        return summary_str.strip()

    def parse_caption_to_dict(self, caption):
        caption_dict = {}
        lines = caption.split("\n")
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                caption_dict[key.strip()] = value.strip()
        return caption_dict