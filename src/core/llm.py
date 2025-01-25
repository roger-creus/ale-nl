import transformers
import torch
from IPython import embed

class LLMAgent():
    def __init__(
        self,
        model_name="meta-llama/Llama-3.2-1B-Instruct",
        env_id="SpaceInvaders",
        action_meanings=None,
        system_prompt_path="prompts/system_prompt_simple.txt",
    ):
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16, 
            max_new_tokens=200
        )
        
        self.env_id = env_id
        self.action_meanings = action_meanings
        print(f"LLM agent {model_name} initialized for {env_id} with actions: {action_meanings}")
        
        with open(system_prompt_path, "r") as f:
            self.system_prompt = f.read()
            self.system_prompt = self.system_prompt.replace("{env_id}", self.env_id)
            self.system_prompt = self.system_prompt.replace("{action_meanings}", str(self.action_meanings))
        
        self.invalid_generation_counter = 0
        
    def generate(self, prompt):
        action_prompt = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        output = self.pipeline(action_prompt, pad_token_id=self.pipeline.tokenizer.eos_token_id)
        output = output[0]['generated_text'][-1]["content"]
        
        try:
            action = int(output)
        except:
            self.invalid_generation_counter += 1
            action = 0
        
        return action
        