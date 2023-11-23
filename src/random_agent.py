import argparse
import os
from nlp.atari_nlp_wrapper import AtariNLPWrapper
from utils import make_env

parser = argparse.ArgumentParser()
parser.add_argument('--env_id', type=str, default='ALE/MsPacman-v5')
parser.add_argument('--seed', type=int, default=1)

if __name__ == '__main__':
    args = parser.parse_args()
    
    # make env
    env = make_env(args)
    env = AtariNLPWrapper(env, args.env_id)

    # init
    obs, _ = env.reset()
    done = False
    ep_reward = 0
    ep_steps = 0

    # store captions
    env_name = args.env_id.split('/')[1]
    if not os.path.exists('captions'):
        os.makedirs('captions')
    f = open(f"captions/{env_name}_captions.txt", "w")
    
    # loop
    while not done:
        action = env.action_space.sample()
        obs, r, term, trunc, info = env.step(action)

        # store metrics
        ep_reward += r
        ep_steps += 1
        done = term or trunc
        
        # store caption
        f.write(info['caption'])
        f.write('====================\n')

        if done:
            break

    print('Episode reward: {}'.format(ep_reward))
    print('Episode steps: {}'.format(ep_steps))
    env.close()
