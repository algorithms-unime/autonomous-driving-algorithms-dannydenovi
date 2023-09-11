import argparse
import gymnasium as gym
from stable_baselines3 import PPO

# Create environment

def train(step, render, domain_randomize):
    env = gym.make("CarRacing-v2", domain_randomize=domain_randomize, verbose=1)
    model = PPO("CnnPolicy", env, verbose=1, tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=step, reset_num_timesteps=False, tb_log_name="ppo")
    model.save("ppo_model")


def retrain(step, render, domain_randomize, model):
    env = gym.make("CarRacing-v2", domain_randomize=domain_randomize,)
    model = PPO.load("ppo_model" , env, verbose=1, tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=step, reset_num_timesteps=False, tb_log_name="ppo")
    model.save("ppo_model")


def test(step, render):
    env = gym.make("CarRacing-v2", domain_randomize=False, render_mode="human")
    model = PPO.load("ppo_model", env, verbose=1)
    obs, _ = env.reset()
    done = False
    while not done:
        env.render()
        action, state = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated , info= env.step(action)
        done = terminated or truncated
    env.close()
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Train or test neural net motor controller.")
    parser.add_argument(
        "--train", dest="train", action="store_true", default=False, help="Train the neural net motor controller"
    )
    parser.add_argument(
        "--test", dest="test", action="store_true", default=False, help="Test the neural net motor controller"
    )
    parser.add_argument(
        "--render", dest="render", action="store_true", default=True, help="Render the gym environment"
    )
    parser.add_argument(
        "--steps", dest="steps", action="store", default=500000, type=int, help="Number of steps to train/test."
    )
    parser.add_argument(
        "--model", dest="model", action="store", default="ppo_model", help="Model file to load"
    )
    parser.add_argument(
        "--domain_randomize", dest="domain_randomize", action="store_true", default=False, help="Domain randomization"
    )
    parser.add_argument("--retrain", dest="retrain", action="store_true", default=False, help="Retrain the model")



    args = parser.parse_args()

    if args.train:
        train(args.steps, args.render, args.domain_randomize)
    elif args.retrain:
        retrain(args.steps, args.render, args.domain_randomize, args.model)
    elif args.test:
        test(args.steps, args.render)
    else:
        parser.print_help()