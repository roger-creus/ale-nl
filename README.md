# Installation

```
conda create -n atari-nlp python=3.8 -y
conda activate atari-nlp
pip install -r requirements.txt
```

# Run random agent and store captions in a file

```
python src/random_agent.py --env_id=<env_name_here>
```

Environments implemented now are ``MsPacmanNoFrameskip-v4`` and ``SpaceInvadersNoFrameskip-v4``. More to implement are [available here](https://gymnasium.farama.org/environments/atari/).

And their corresponding RAM annotations can be found [here](https://github.com/mila-iqia/atari-representation-learning/blob/master/atariari/benchmark/ram_annotations.py)