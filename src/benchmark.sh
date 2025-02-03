#!/bin/bash

# List of environments
envs=(
  "SpaceInvaders"
)

# List of model names
models=(
  "meta-llama/Llama-3.2-1B-Instruct"
  #"meta-llama/Llama-3.3-70B-Instruct"
  "meta-llama/Llama-3.2-3B-Instruct"
  "meta-llama/Llama-3.1-8B-Instruct"
  "microsoft/phi-4"
  "microsoft/Phi-3.5-mini-instruct"
  "mistralai/Mixtral-8x7B-Instruct-v0.1"
)

# List of context lengths
context_lengths=(0)

# List of prompt chains
prompt_chains=(
  "prompt_chains/simple"
  "prompt_chains/think_stepbystep"
  "prompt_chains/cot"
)

temperatures=(
  0.0
  0.5
  1.0
)

# Loop through all combinations of envs, models, and context_lengths
for env in "${envs[@]}"; do
  for prompt_chain in "${prompt_chains[@]}"; do
    for temperature in "${temperatures[@]}"; do
      for model in "${models[@]}"; do
        for context_length in "${context_lengths[@]}"; do
          echo "Running evaluation for Env: $env, Model: $model, Context Length: $context_length, Prompt Chain: $prompt_chain"
          python src/agents/eval_agent.py --env_id "$env" --model_name "$model" --context_length "$context_length" --prompt_chain "$prompt_chain" --temperature "$temperature" --num_episodes=3 
        done
      done
    done
  done
done