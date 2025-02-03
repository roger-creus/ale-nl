import transformers
import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.core.logger_utils import log_chain
from IPython import embed


class LLMAgent():
    def __init__(
        self,
        model_name="meta-llama/Llama-3.2-1B-Instruct",
        env_id="SpaceInvaders",
        action_meanings=None,
        prompt_chain_path="prompt_chains/simple",
        save_dir="results",
        temperature=0.1,
    ):
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Create pipeline using pre-loaded model
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.bfloat16,
            max_new_tokens=512,
            do_sample=True,
            temperature=temperature,
        )

        # load prompt chain
        self.prompt_chain = []
        prompt_chain_files = sorted(os.listdir(prompt_chain_path), key=lambda x: int(x.split('_')[0]))
        for file in prompt_chain_files:
            with open(os.path.join(prompt_chain_path, file), 'r') as f:
                self.prompt_chain.append(f.read())
                
        # misc
        self.temperature = temperature
        self.env_id = env_id
        self.action_meanings = action_meanings
        print(f"LLM agent {model_name} initialized for {env_id}")
        self.save_dir = save_dir
        self.invalid_generation_counter = 0
        self.logs = []
                
    def generate(self, observation):
        llm_chain = [
            {"role": "system", "content": f"You are playing {self.env_id}. The available actions are: {self.action_meanings}."},
        ]
        
        for i, prompt in enumerate(self.prompt_chain):
            llm_chain.append({"role": "user", "content": prompt})
            if i == 0:
                llm_chain[-1]["content"] = llm_chain[-1]["content"] + "\n\n" + observation

            if i == len(self.prompt_chain) - 1:
                llm_chain[-1]["content"] = llm_chain[-1]["content"] + "\n\n" + "Remember the available actions are: " + str(self.action_meanings)

            output = self.pipeline(llm_chain, pad_token_id=self.pipeline.tokenizer.eos_token_id, temperature=self.temperature, do_sample=True)
            output = output[0]['generated_text'][-1]["content"]
            llm_chain.append({"role": "assistant", "content": output})
                
        # we expect that the output of the last prompt in the chain is the action
        try:
            action = int(output)
        except:
            self.invalid_generation_counter += 1
            action = 0
            
        # logging
        llm_chain[-1]["content"] = f"{self.action_meanings[action]}"
        self.logs.append(log_chain(llm_chain))
        return action
    
    def get_logs(self):
        cp_logs = self.logs.copy()
        self.logs = []
        return cp_logs