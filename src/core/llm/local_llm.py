import torch
import transformers
from src.core.llm.base_llm import LLMAgent
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor
from src.core.utils import log_chain

class LocalLLMAgent(LLMAgent):
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
        super().__init__(model_name, env_id, action_meanings, prompt_chain_path, save_dir, temperature, max_new_tokens)
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            attn_implementation="flash_attention_2",
            device_map="auto"
        )
        print(f"{model_name} initialized for {env_id}")
        
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            processor=self.processor,
            torch_dtype=torch.bfloat16,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            pad_token_id=(self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None 
                          else self.tokenizer.eos_token_id)
        )
    
    def generate(self, observation):
        llm_chain = []
        for i, prompt in enumerate(self.prompt_chain):
            # Build the chain of prompts
            llm_chain.append({
                "role": "user",
                "content": prompt
            })
            # For the first prompt, add game context and observation
            if i == 0:
                llm_chain[-1]["content"] = (
                    f"You are playing {self.env_id}. {self.game_description}\n"
                    f"The available actions are: {self.action_meanings}. In our coordinate system, "
                    f"(x=0, y=0) is at the upper left corner of the screen, and as x and y increase, positions "
                    f"move toward the lower right corner.\n"
                    f"{llm_chain[-1]['content']}\n{observation}"
                )
            # For the last prompt, add reminder of available actions
            if i == len(self.prompt_chain) - 1:
                llm_chain[-1]["content"] += f"\nRemember the available actions are: {self.action_meanings}"
            
            # Generate output using the local pipeline
            output = self.pipeline(llm_chain)
            output_text = output[0]['generated_text'] if isinstance(output, list) else output
            llm_chain.append({"role": "assistant", "content": output_text})
        
        # Extract action from the final output
        try:
            action_idx = int(output_text[-1]["content"].split("ACTION:")[1].strip())
            semantic_action = self.action_meanings[action_idx]
        except (ValueError, IndexError):
            self.invalid_generation_counter += 1
            action_idx = 0
            semantic_action = "NOOP"
        
        # Replace last assistant message with the final semantic action
        llm_chain[-1]["content"] = semantic_action
        self.logs.append(log_chain(llm_chain))
        return action_idx