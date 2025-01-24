#!/bin/bash

# List of environments
envs=(
  "SpaceInvaders"
)

# List of model names
models=(
  "meta-llama/Llama-3.2-1B-Instruct"
  "meta-llama/Llama-3.2-3B-Instruct"
  "meta-llama/Llama-3.1-8B-Instruct"
  "microsoft/phi-4"
  "microsoft/Phi-3.5-mini-instruct"
)

# List of context lengths
context_lengths=(0 1 2 3 4 5)

# Loop through all combinations of envs, models, and context_lengths
for env in "${envs[@]}"; do
  for model in "${models[@]}"; do
    for context_length in "${context_lengths[@]}"; do
      echo "Running evaluation for Env: $env, Model: $model, Context Length: $context_length"
      python src/agents/eval_agent.py --env_id "$env" --model_name "$model" --context_length "$context_length"
    done
  done
done
