from gym.envs.registration import register

register(
    id='DroneEnv-v0',
    entry_point='droneenv.droneEnv:DroneEnv',
)
