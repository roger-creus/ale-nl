#!/bin/bash

# List of environments
envs=(
  "SpaceInvaders"
  "MsPacman"
  "Seaquest"
  "Freeway"
  "Asterix"
  "BattleZone"
  "Bowling"
  "BeamRider"
)

# List of model names
models=(
  "meta-llama/Llama-3.2-1B-Instruct"
  "Qwen/Qwen2.5-0.5B-Instruct"
  "meta-llama/Llama-3.2-3B-Instruct"
  #"microsoft/phi-4"
  #"Qwen/Qwen2.5-14B-Instruct"
  #"mistralai/Mixtral-8x7B-Instruct-v0.1"
  #"microsoft/Phi-3.5-mini-instruct"
  #"meta-llama/Meta-Llama-3-8B-Instruct"
  #"deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
  #"deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
)

# List of context lengths
context_lengths=(0 1 5)

# List of prompt chains
prompt_chains=(
  "prompt_chains/simple"
  # "prompt_chains/think_stepbystep"
  # "prompt_chains/cot"
)

temperatures=(
  0.01
  0.6
  #1.0
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