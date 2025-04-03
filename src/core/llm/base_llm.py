import os
import transformers
import torch
from abc import ABC, abstractmethod
from openai import OpenAI
from transformers import AutoProcessor, AutoTokenizer, AutoModelForCausalLM
from src.core.utils import log_chain 
from IPython import embed

class LLMAgent(ABC):
    def __init__(
        self,
        model_name,
        env_id,
        action_meanings,
        prompt_chain_path,
        save_dir,
        temperature=0.6,
        max_new_tokens=512
    ):
        # Common initialization for all LLM agents
        self.model_name = model_name
        self.env_id = env_id
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.action_meanings = action_meanings
        self.save_dir = save_dir
        self.invalid_generation_counter = 0
        self.logs = []
        
        # Load game description (this is common across agents)
        game_desc_path = os.path.join("src", "captions", "game_descriptions", f"{env_id}.txt")
        with open(game_desc_path, "r") as f:
            self.game_description = f.read()
        
        # Load prompt chain (this is common across agents)
        self.prompt_chain = []
        prompt_chain_files = sorted(
            os.listdir(prompt_chain_path),
            key=lambda x: int(x.split('_')[0])
        )
        for file in prompt_chain_files:
            with open(os.path.join(prompt_chain_path, file), 'r') as f:
                self.prompt_chain.append(f.read())
    
    @abstractmethod
    def generate(self, observation):
        """
        Generate an action based on the provided observation.
        This method must be implemented by subclasses.
        """
        pass

    def get_logs(self):
        cp_logs = self.logs.copy()
        invalid_counter = self.invalid_generation_counter
        self.invalid_generation_counter = 0
        self.logs = []
        return cp_logs, invalid_counter