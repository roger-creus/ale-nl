import argparse
import os
import imageio
from env import make_env
from nlp.ale_nlp_wrapper import ALENLPWrapper

parser = argparse.ArgumentParser()
parser.add_argument('--env_id', type=str, default='MsPacman')
parser.add_argument('--num_episodes', type=int, default=5)
parser.add_argument('--seed', type=int, default=1)

# nlp
parser.add_argument('--context_length', type=int, default=0)

# logging
parser.add_argument('--store_video', type=bool, default=False)
parser.add_argument('--store_captions', type=bool, default=True)
parser.add_argument('--save_dir', type=str, default='output')

if __name__ == '__main__':
    args = parser.parse_args()
    args.env_id = f'{args.env_id}NoFrameskip-v4'

    # Create output directory if it doesn't exist
    os.makedirs(args.save_dir, exist_ok=True)

    # make env
    env = make_env(args)
    env = ALENLPWrapper(
        env, 
        args.env_id, 
        context_length=args.context_length,
        store_captions=args.store_captions,
        save_dir=args.save_dir
    )

    # loop
    ep_rewards = []
    ep_lengths = []

    for episode in range(args.num_episodes):
        obs, info = env.reset()
        done = False
        ep_r = 0
        ep_l = 0
        frames = []  # Store frames for this episode

        while not done:
            if args.store_video:
                frames.append(env.render())

            # step simulation
            action = env.action_space.sample()
            obs, r, term, trunc, info = env.step(action)

            # store metrics
            ep_r += r
            ep_l += 1
            done = term or trunc

        # Save GIF after each episode
        if args.store_video and frames:
            gif_path = os.path.join(args.save_dir, f'episode_{episode}.gif')
            imageio.mimsave(gif_path, frames, fps=30)
            print(f'Saved GIF for episode {episode} at {gif_path}')

        print('Episode: {}, Reward: {}, Length: {}'.format(episode, ep_r, ep_l))
        ep_rewards.append(ep_r)
        ep_lengths.append(ep_l)

    print('====================')
    print('Mean Episode Reward: {}'.format(sum(ep_rewards) / len(ep_rewards)))    
    print('Mean Episode Length: {}'.format(sum(ep_lengths) / len(ep_lengths)))
    env.close()