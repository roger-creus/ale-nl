import transformers
import torch
from IPython import embed

class LLMAgent():
    def __init__(
        self,
        model_name="meta-llama/Llama-3.2-1B-Instruct",
        env_id="SpaceInvaders",
        action_meanings=None
    ):
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16, 
        )
        
        self.env_id = env_id
        self.action_meanings = action_meanings
        print(f"LLM agent {model_name} initialized for {env_id} with actions: {action_meanings}")
        
        self.invalid_generation_counter = 0
        
    def generate(self, prompt):
        action_prompt = [
            {"role": "system", "content": f"You are playing {self.env_id}. You have to decide on the next action to take. The possible actions are: {self.action_meanings}. Answer with only the index of the action you want to take or otherwise the action will be ignored. Do not include any other information other than the selected action index integer."}, 
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
        