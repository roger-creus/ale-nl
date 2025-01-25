import argparse
import os
import imageio

from src.env.env import make_env
from src.env.ale_nlp_wrapper import ALENLPWrapper

parser = argparse.ArgumentParser()
parser.add_argument('--env_id', type=str, default='SpaceInvaders')
parser.add_argument('--num_episodes', type=int, default=5)
parser.add_argument('--seed', type=int, default=1)

if __name__ == '__main__':
    args = parser.parse_args()

    # create save directory
    args.save_dir = os.path.join('results', "random", args.env_id)
    os.makedirs(args.save_dir, exist_ok=True)
    env_name = args.env_id
    args.env_id = f'{args.env_id}NoFrameskip-v4'
    
    # make env
    env = make_env(args)
    env = ALENLPWrapper(
        env, 
        args.env_id, 
        context_length=0
    )

    # loop
    ep_rewards = []
    ep_lengths = []
    for episode in range(args.num_episodes):
        obs, info = env.reset()
        done = False
        ep_r = 0
        ep_l = 0
        frames = []

        while not done:
            frames.append(env.render())

            # step simulation
            action = env.action_space.sample()
            obs, r, term, trunc, info = env.step(action)

            # store metrics
            ep_r += r
            ep_l += 1
            done = term or trunc

        # save gif
        gif_path = os.path.join(args.save_dir, f'episode_{episode}.gif')
        imageio.mimsave(gif_path, frames, fps=30)

        # print metrics
        print('Episode: {}, Reward: {}, Length: {}'.format(episode, ep_r, ep_l))
        ep_rewards.append(ep_r)
        ep_lengths.append(ep_l)

    # store aggregated metrics to csv
    print('====================')
    mean_reward = sum(ep_rewards) / len(ep_rewards)
    std_reward = (sum([(r - mean_reward) ** 2 for r in ep_rewards]) / len(ep_rewards)) ** 0.5
    mean_length = sum(ep_lengths) / len(ep_lengths)
    std_length = (sum([(l - mean_length) ** 2 for l in ep_lengths]) / len(ep_lengths)) ** 0.5
    print(f'Mean Reward: {mean_reward}, Std Reward: {std_reward}')
    print(f'Mean Length: {mean_length}, Std Length: {std_length}')
    
    with open(os.path.join(args.save_dir, 'metrics.csv'), 'w') as f:
        f.write('model_name,env_id,sys_prompt,context_length,episode_reward,episode_length\n')
        for i in range(args.num_episodes):
            f.write(f'random,{env_name},none,none,{ep_rewards[i]},{ep_lengths[i]}\n')
   
    env.close()