import argparse
import os
import imageio
import matplotlib.pyplot as plt
import time

from src.env.env import make_env
from src.core.llm import LLMAgent
from src.env.ale_nlp_wrapper import ALENLPWrapper

from IPython import embed

parser = argparse.ArgumentParser()
parser.add_argument('--env_id', type=str, default='SpaceInvaders')
parser.add_argument('--num_episodes', type=int, default=5)
parser.add_argument('--seed', type=int, default=1)

# nlp
parser.add_argument('--model_name', type=str, default='Qwen/Qwen2.5-0.5B-Instruct')
parser.add_argument('--temperature', type=float, default=0.01)
parser.add_argument('--context_length', type=int, default=0)
parser.add_argument('--prompt_chain_path', type=str, default='prompt_chains/simple')

if __name__ == '__main__':
    args = parser.parse_args()

    # create save directory
    args.save_dir = os.path.join(
        'results',
        args.model_name.split('/')[-1],
        args.env_id,
        args.prompt_chain_path.split("/")[-1],
        f"temperature_{args.temperature}",
        f'contextLen_{args.context_length}'
    )
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
        prompt_chain_path=args.prompt_chain_path,
        temperature=args.temperature,
    )
    
    # loop
    ep_rewards = []
    ep_lengths = []
    generation_time = time.time()
    for episode in range(args.num_episodes):
        obs, info = env.reset()
        done = False
        ep_r = 0
        ep_l = 0
        frames = []
        c = 0
        while not done:
            c += 1
            # record frames
            frames.append(env.render())

            # query LLM agent
            action = agent.generate(info['caption'])
            # round float
            print(f'=== Step {c} | Action: {action} | Inference Time: {round(time.time() - generation_time, 2)}s ===')
            generation_time = time.time()
            
            # step environment
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
        logs, invalid_generation_counts = agent.get_logs() 
        with open(caption_path, 'w') as f:
            f.write('\n'.join(logs))
            
        # save percentage of invalid generations as plot (percentage over episode length)
        plt.figure()
        plt.bar(['Invalid Generations', 'Valid Generations'], [invalid_generation_counts, ep_l - invalid_generation_counts])
        plt.title(f'Invalid Generation Percentage for Episode {episode}')
        plt.xlabel('Generation Type')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig(os.path.join(args.save_dir, f'episode_{episode}_invalid_generation_count.png'))
        
        # save action distribution
        all_actions = {env.action_meanings[i]: 0 for i in range(env.action_space.n)}
        for log in logs:
            action = log.split('\nassistant: ')[-1].split('\n')[0]
            try:
                all_actions[action] += 1
            except:
                continue
        
        all_actions = dict(sorted(all_actions.items(), key=lambda item: item[1], reverse=True))
        plt.figure()
        plt.bar(all_actions.keys(), all_actions.values())
        plt.xticks(rotation=45)
        plt.title(f'Action Distribution for Episode {episode}')
        plt.xlabel('Action')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(os.path.join(args.save_dir, f'episode_{episode}_action_distribution.png'))
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
        f.write('model_name,env_id,prompt_chain,temperature,context_length,episode_reward,episode_length\n')
        for episode in range(args.num_episodes):
            f.write(f'{args.model_name},{env_name},{args.prompt_chain_path.split("/")[-1]},{args.temperature},{args.context_length},{ep_rewards[episode]},{ep_lengths[episode]}\n')
   
    env.close()