import argparse
import gymnasium as gym
from stable_baselines3 import DQN

# Create environment

def train(step):
    env = gym.make("CarRacing-v2", domain_randomize=False, verbose=1, continuous=False)
    model = DQN("CnnPolicy", env, verbose=1, tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=step, reset_num_timesteps=False, tb_log_name="dqn")
    model.save("dqn_model")


def retrain(step, loaded_model):
    env = gym.make("CarRacing-v2", domain_randomize=False, continuous=False)
    model = DQN.load(loaded_model , env, verbose=1, tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=step, reset_num_timesteps=False, tb_log_name="dqn")
    model.save(loaded_model)


def test(loaded_model):
    env = gym.make("CarRacing-v2", domain_randomize=False, render_mode="human", continuous=False)
    model = DQN.load(loaded_model, env, verbose=1)
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
        "--steps", dest="steps", action="store", default=500000, type=int, help="Number of steps to train/test."
    )
    parser.add_argument(
        "--model", dest="model", action="store", default="dqn_model", help="Model file to load"
    )
    parser.add_argument("--retrain", dest="retrain", action="store_true", default=False, help="Retrain the model")



    args = parser.parse_args()

    if args.train:
        train(args.steps)
    elif args.retrain:
        retrain(args.steps, args.model)
    elif args.test:
        test(args.model)
    else:
        parser.print_help()