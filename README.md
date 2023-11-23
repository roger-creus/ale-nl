# Installation

```
conda create -n atari-nlp python=3.8
conda activate atari-nlp
pip install -r requirements.txt
pip install gymnasium[atari]
pip install gymnasium[accept-rom-license]
```

# Run random agent and store captions in a file

```
python src/random_agent.py --env_id=<env_name_here>
```

Environments implemented now are ``ALE/MsPacman-v5`` and ``ALE/SpaceInvaders-v5``. More to implement are [available here](https://gymnasium.farama.org/environments/atari/).

And their corresponding RAM annotations can be found [here](https://github.com/mila-iqia/atari-representation-learning/blob/master/atariari/benchmark/ram_annotations.py)