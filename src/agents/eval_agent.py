import argparse
import os
import imageio
import matplotlib.pyplot as plt

from src.env.env import make_env
from src.core.llm import LLMAgent
from src.env.ale_nlp_wrapper import ALENLPWrapper

parser = argparse.ArgumentParser()
parser.add_argument('--env_id', type=str, default='SpaceInvaders')
parser.add_argument('--num_episodes', type=int, default=5)
parser.add_argument('--seed', type=int, default=1)

# nlp
parser.add_argument('--model_name', type=str, default='meta-llama/Llama-3.2-1B-Instruct')
parser.add_argument('--context_length', type=int, default=0)
parser.add_argument('--system_prompt_path', type=str, default='prompts/system_prompt_simple.txt')

if __name__ == '__main__':
    args = parser.parse_args()

    # create save directory
    args.save_dir = os.path.join('results', args.model_name.split('/')[-1], args.env_id, f'contextLen_{args.context_length}')
    os.makedirs(args.save_dir, exist_ok=True)
    env_name = args.env_id
    args.env_id = f'{args.env_id}NoFrameskip-v4'
    
    # make env
    env = make_env(args)
    env = ALENLPWrapper(
        env, 
        args.env_id, 
        context_length=args.context_length,
    )

    # make LLM agent
    agent = LLMAgent(
        model_name=args.model_name,
        env_id=env_name,
        action_meanings=env.action_meanings,
        system_prompt_path=args.system_prompt_path,
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
        captions = []
        llm_actions = []

        while not done:
            frames.append(env.render())

            # step simulation
            captions.append(info['caption'])
            action = agent.generate(info['caption'])
            llm_actions.append(env.action_meanings[action])
            obs, r, term, trunc, info = env.step(action)

            # store metrics
            ep_r += r
            ep_l += 1
            done = term or trunc

        # save gif
        gif_path = os.path.join(args.save_dir, f'episode_{episode}.gif')
        imageio.mimsave(gif_path, frames, fps=30)
        
        # save captions
        caption_path = os.path.join(args.save_dir, f'episode_{episode}_captions.txt')
        with open(caption_path, 'w') as f:
            for caption, action in zip(captions, llm_actions):
                f.write(f'{caption}\n')
                f.write(f'LLM Action: {action}\n====================\n')
            f.write(f'Invalid generations in this episode: {agent.invalid_generation_counter}')
        
        # save action distribution (histogram)
        action_freq = {action: llm_actions.count(action) for action in set(llm_actions)}
        action_freq = {k: v for k, v in sorted(action_freq.items(), key=lambda item: item[1], reverse=True)}
        plt.figure()
        plt.bar(action_freq.keys(), action_freq.values())
        plt.title('Action Distribution')
        plt.xlabel('Action')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(args.save_dir, f'episode_{episode}_actions.png'))
        plt.close()
        
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
        for episode in range(args.num_episodes):
            f.write(f'{args.model_name},{env_name},{args.system_prompt_path.split("/")[-1].split(".")[-2]},{args.context_length},{ep_rewards[episode]},{ep_lengths[episode]}\n')
   
    env.close()