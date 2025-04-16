# 🎮 ALE-NL: The Arcade Learning Environment in Natural Language

**ALE-NL** supports the Arcade Learning Environment (ALE) with Large Language Models (LLMs), enabling LLMs to **interact with and be evaluated on Atari games** through natural language. Built on top of [OCAtari](https://github.com/k4ntz/OC_Atari), it allows systematic, interpretable, and **reproducible** benchmarking of LLMs in classic Atari games.

<table>
<tr>
<td><img src="static/gpt4o_spaceinvaders.gif" width="100%"/></td>
<td><img src="static/qwen05_spaceinvaders.gif" width="100%"/></td>
<td><img src="static/qwen14_battlezone.gif" width="100%"/></td>
<td><img src="static/qwen14_beamrider.gif" width="100%"/></td>
</tr>
<tr>
<td><img src="static/qwen14_boxing.gif" width="100%"/></td>
<td><img src="static/qwen14_freeway.gif" width="100%"/></td>
<td><img src="static/qwen14_kungfu.gif" width="100%"/></td>
<td><img src="static/qwen14_mspacman.gif" width="100%"/></td>
</tr>
</table>

---

## 🧠 Overview

ALE-NL translates game states into natural language descriptions that are easy to consume for LLMs. It provides a simple yet powerful interface to:

- Benchmark LLMs on Atari tasks 🏆
- Analyze and visualize behavior 🤖📊
- Reproduce results with ease 🔁

<p align="center">
  <img src="static/alenl_diagram.png" width="70%"/>
</p>

---

## ✅ Features

- [x] 12 Atari games supported (adding more!):  
  `Asterix`, `BattleZone`, `BeamRider`, `Bowling`, `Boxing`, `Breakout`, `DemonAttack`, `Freeway`, `KungfuMaster`, `MsPacman`, `Seaquest`, `SpaceInvaders`
- [x] Run any HuggingFace `text-generation` model locally 💻
- [x] Run OpenAI models via API ☁️
- [x] Modular and customizable prompting strategies (CoT, zero-shot, few-shot)
- [x] Easy ablation of sampling parameters (temperature, context length, etc.)
- [x] One-click benchmarking: [`plot_benchmark_results.ipynb`](plot/plot_benchmark_results.ipynb)
- [x] Visual + statistical debugging:  
  - [Action distributions](static/gpt4o_actiondist.png)  
  - [Generation errors](static/gpt4o_generation_errors.png)  
  - [Full interaction traces](static/gpt4o_spaceinvaders_interaction_trace.txt)  

---

## ✨ Prompting Pipeline

Prompt templates are modularly composed from:

1. **Game Descriptions**: Loaded from `src/captions/game_descriptions/` (from [ALE docs](https://ale.farama.org/environments/)).
2. **Prompt Chains**: Found in `prompt_chains/` to enable CoT, zero-shot, few-shot, etc.
3. **State Descriptions**: Defined per game in `src/captions/games/`. Customizable for each game.

<p align="center">
  <img src="static/static/prompting.png" width="70%"/>
</p>

---

## ⚙️ Installation

We recommend using `conda`, but any Python 3.8+ virtual environment should work.

```bash
conda create -n ale-nlp python=3.8 -y
conda activate ale-nlp
```

### 🧠 Running LLMs Locally

Install dependencies with CUDA support:

```bash
conda install -c conda-forge cudatoolkit-dev
pip install transformers[torch]
pip install -r requirements_local.txt
```

### ☁️ Running OpenAI Models

Only requires OpenAI's API client:

```bash
pip install -r requirements_api.txt
```

Make sure to set your OpenAI API key.

### 🔁 Final Setup

```bash
pip install -e .
```

---

## 🚀 Running

Running any LLM in an Atari game is just one command away!  
Simply pass the appropriate model name and environment ID to `src/run.py`:

- **`<LLM_NAME>`**: Must be a valid model ID from either:
  - 🤗 HuggingFace (e.g., `Qwen/Qwen2-0.5B`)
  - 🧠 OpenAI (e.g., `gpt-3.5-turbo-0125`)

- **`<ENV_ID>`**: The Atari game name (e.g., `SpaceInvaders`, `MsPacman`, `Asterix`, ...)

```bash
python src/run.py --model_name=<LLM_NAME> --env_id=<ENV_ID>
```

Additional options can be passed for fine-grained control:
- `--prompt_chain_path`: Selects a prompting strategy
- `--temperature`: Controls sampling randomness
- `--context_length`: Limits the LLM input length
- _...and more!_

📁 All logs, outputs, and interaction traces will be automatically saved in the specified `--save_dir`.

👉 For the full list of options, check [`src/run.py`](src/run.py).

## 📬 Contribute or Explore More

Got a new game, prompt strategy, or LLM you want to try? Contributions and suggestions are welcome!

---

---

## 📚 Citation

If you use **ALE-NL** in your research, please consider citing it using the following format:

```bibtex
@misc{ale-nl2025,
  title     = {ALE-NL: The Arcade Learning Environment in Natural Language},
  author    = {Creus Castanyer, Roger},
  year      = {2025},
  url       = {https://github.com/roger-creus/ale-nl},
  note      = {Accessed: 2025-04-16}
}
```