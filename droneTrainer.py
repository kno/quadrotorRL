import gym,time
import droneenv

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

env = gym.make("DroneEnv-v0")
nb_actions = env.action_space.n
# Option 1 : Simple model
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))


for i_episode in range(1):
    observation = env.reset()
    for t in range(2):
        env.render()
#        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            env.reset()
            break
time.sleep(10)
env.stop()
