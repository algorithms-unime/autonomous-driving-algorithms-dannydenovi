import argparse
import uuid
import gym_donkeycar
import gym
import os
from stable_baselines3 import PPO

if __name__ == "__main__":




    # Graficare reward, loss (FATTO)
    # Qual è la terminazione? (FATTO)
    # ricerca su generalizzazione PPO
    # PPO transfer learning


    # Initialize the donkey environment
    # where env_name one of:

    env_list = [
        "donkey-warehouse-v0",
        "donkey-generated-roads-v0",
        "donkey-avc-sparkfun-v0",
        "donkey-generated-track-v0",
        "donkey-roboracingleague-track-v0",
        "donkey-waveshare-v0",
        "donkey-minimonaco-track-v0",
        "donkey-warren-track-v0",
        "donkey-thunderhill-track-v0",
        "donkey-circuit-launch-track-v0",
    ]

    body_style = [
        "donkey",
        "bare",
        "f1", 
        "car01",
        "cybertruck"
    ]

    parser = argparse.ArgumentParser(description="ppo_train")
    parser.add_argument("--port", type=int, default=9091, help="port to use for tcp")
    parser.add_argument("--test", action="store_true", help="load the trained model and play")
    parser.add_argument("--multi", action="store_true", help="start multiple sims at once")
    parser.add_argument("--env_name", type=str, default="donkey-warehouse-v0", help="name of donkey sim environment", choices=env_list)
    parser.add_argument("--bstyle", type=str, default="f1", help="name of car body type", choices=body_style)
    parser.add_argument("--retrain", action="store_true", help="load the trained model and retrain")
    parser.add_argument("--lidar", action="store_true", help="Enable lidar visualization")
    parser.add_argument("--load_model", type=str, default="ppo_donkey", help="Specify path for model")

    args = parser.parse_args()
    env_id = args.env_name

    conf = {
        "host": "host.docker.internal",
        "port": args.port,
        "body_style": args.bstyle,
        "body_rgb": (228, 0, 43),
        "car_name": "PPO",
        "font_size": 50,
        "racer_name": "PPO",
        "country": "USA",
        "bio": "Learning to drive w PPO RL",
        "guid": str(uuid.uuid4()),
        "max_cte": 10
    }

    if(args.lidar):
        conf["lidar_config"] = {
                "deg_per_sweep_inc": 2.0,
                "deg_ang_down": 0.0,
                "deg_ang_delta": -1.0,
                "num_sweeps_levels": 1,
                "max_range": 50.0,
                "noise": 0.4,
                "offset_x": 0.0,
                "offset_y": 0.5,
                "offset_z": 0.5,
                "rot_x": 0.0,   
            }



    if args.test:
        # Make an environment test our trained policy
        env = gym.make(args.env_name, conf=conf)        
        model = PPO.load(args.load_model, env=env)

        obs = env.reset()
        for _ in range(2000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            if done:
                obs = env.reset()

        print("done testing")
    else:
        # Make an environment to train our agent
        env = gym.make(args.env_name, conf=conf)

        if args.retrain:
            os.system('cp ppo_donkey.zip ppo_donkey.zip.old')
            model = PPO.load(env.load_model, env=env,  tensorboard_log="./ppo_donkeycar_tensorboard/")
        else:
            model = PPO("CnnPolicy", env, verbose=1,  tensorboard_log="./ppo_donkeycar_tensorboard/")

        model.learn(total_timesteps=10000, reset_num_timesteps=False)

        obs = env.reset()

        for i in range(1000):

            action, _states = model.predict(obs, deterministic=True)

            obs, reward, done, info = env.step(action)

            try:
                env.render()
            except Exception as e:
                print(e)
                print("failure in render, continuing...")

            if done:
                obs = env.reset()

            if i % 100 == 0:
                print("saving...")
                model.save("ppo_donkey")

        # Save the agent
        model.save("ppo_donkey")
        print("done training")

    env.close()
