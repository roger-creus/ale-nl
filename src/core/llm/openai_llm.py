from src.core.llm.base_llm import LLMAgent
from openai import OpenAI
from src.core.utils import log_chain
from IPython import embed

class OpenAIAgent(LLMAgent):
    def __init__(
        self,
        model_name="gpt-3.5-turbo",
        env_id="SpaceInvaders",
        action_meanings=None,
        prompt_chain_path="prompt_chains/simple",
        save_dir="results",
        temperature=0.6,
        max_new_tokens=512
    ):
        super().__init__(model_name, env_id, action_meanings, prompt_chain_path, save_dir, temperature, max_new_tokens)
        self.client = OpenAI()
        print(f"OpenAIAgent using {model_name} initialized for {env_id}")
    
    def generate(self, observation):
        llm_chain = []
        for i, prompt in enumerate(self.prompt_chain):
            # Append prompt to chain
            llm_chain.append({
                "role": "user",
                "content": prompt
            })
            # For first prompt, add game context and observation
            if i == 0:
                llm_chain[-1]["content"] = (
                    f"You are playing {self.env_id}. {self.game_description}\n"
                    f"The available actions are: {self.action_meanings}. In our coordinate system, "
                    f"(x=0, y=0) is at the upper left corner of the screen, and as x and y increase, positions "
                    f"move toward the lower right corner.\n"
                    f"{llm_chain[-1]['content']}\n{observation}"
                )
            # For last prompt, add reminder of available actions
            if i == len(self.prompt_chain) - 1:
                llm_chain[-1]["content"] += f"\nRemember the available actions are: {self.action_meanings}"
            
            # Query the OpenAI API using the current message chain
            try:
                # First try with temperature
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=llm_chain,
                    temperature=self.temperature,
                    max_tokens=self.max_new_tokens
                )
            except:
                try:
                    # If temperature fails, try without it
                    completion = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=llm_chain,
                        max_tokens=self.max_new_tokens
                    )
                except:
                    # If max_tokens fails, try with max_completion_tokens
                    completion = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=llm_chain,
                        max_completion_tokens=self.max_new_tokens
                    )
                
            # Get the assistant's reply from the response
            response_message = completion.choices[0].message
            llm_chain.append({
                "role": response_message.role,
                "content": response_message.content
            })
        
        # Extract action from the final output
        final_output = llm_chain[-1]["content"]
        
        try:
            action_idx = int(final_output.split("ACTION:")[1].strip())
            semantic_action = self.action_meanings[action_idx]
        except (ValueError, IndexError):
            self.invalid_generation_counter += 1
            action_idx = 0
            semantic_action = "NOOP"
        
        # Replace last assistant message with the final semantic action
        llm_chain[-1]["content"] = semantic_action
        self.logs.append(log_chain(llm_chain))
        return action_idx