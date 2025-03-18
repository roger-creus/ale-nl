import transformers
import torch
import os
from transformers import AutoProcessor, AutoTokenizer, AutoModelForCausalLM

from src.core.utils import log_chain
from IPython import embed

class LLMAgent():
    def __init__(
        self,
        model_name="Qwen/Qwen2.5-0.5B-Instruct",
        env_id="SpaceInvaders",
        action_meanings=None,
        prompt_chain_path="prompt_chains/simple",
        save_dir="results",
        temperature=0.6,
        max_new_tokens=512
    ):
        # misc
        self.env_id = env_id
        self.temperature = temperature
        self.max_new_tokens = max_new_tokens
        self.action_meanings = action_meanings
        self.save_dir = save_dir
        self.game_description = open(f"src/captions/game_descriptions/{env_id}.txt", "r").read()
        self.invalid_generation_counter = 0
        self.logs = []
        
        # create model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
            device_map="auto"
        )
        print(f"{model_name} initialized for {env_id}")
            
        # create processor
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # load prompt chain
        self.prompt_chain = []
        prompt_chain_files = sorted(os.listdir(prompt_chain_path), key=lambda x: int(x.split('_')[0]))
        for file in prompt_chain_files:
            with open(os.path.join(prompt_chain_path, file), 'r') as f:
                self.prompt_chain.append(f.read())
                
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            processor=self.processor,
            torch_dtype=torch.bfloat16,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            pad_token_id=self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None else self.tokenizer.eos_token_id, 
        )
        
    def generate(self, observation):
        llm_chain = []

        for i, prompt in enumerate(self.prompt_chain):
            llm_chain.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            # Add intro and observation to the first prompt
            if i == 0:
                llm_chain[-1]["content"] = (
                    f"You are playing {self.env_id}. {self.game_description}\n"
                    f"The available actions are: {self.action_meanings}. In our coordinate system, (x=0, y=0) is at the upper left corner of the screen, and as x and y increase, positions move toward the lower right corner.\n"
                    f"{llm_chain[-1]['content']}\n{observation}"
                )

            # Add reminder of actions to the last prompt
            if i == len(self.prompt_chain) - 1:
                llm_chain[-1]["content"] += f"\nRemember the available actions are: {self.action_meanings}"

            output = self.pipeline(llm_chain)
                
            output = output[0]['generated_text'][-1]["content"] if isinstance(output, list) else output
            llm_chain.append({"role": "assistant", "content": output})

        # Extract action from the last output
        try:
            action_idx = int(output.split("ACTION:")[1].strip())
            semantic_action = self.action_meanings[action_idx]
        except (ValueError, IndexError):
            self.invalid_generation_counter += 1
            action_idx = 0
            semantic_action = "NOOP"

        llm_chain[-1]["content"] = semantic_action
        self.logs.append(log_chain(llm_chain))
        return action_idx
    
    def get_logs(self):
        cp_logs = self.logs.copy()
        invalid_generation_counter = self.invalid_generation_counter
        self.invalid_generation_counter = 0
        self.logs = []
        return cp_logs, invalid_generation_counter