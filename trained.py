import gym
from keras.models import load_model
from keras.layers import Flatten

import numpy as np
import tensorflow as tf
import time
#model = load_model('cartpole_weight.h5')
model = load_model('my_model.h5')

env = gym.make('CartPole-v1')
# print(env.action_space.)
# #> Discrete(2)
# print(env.observation_space)
# #> Box(4,)
observation = env.reset()
env.render()
time.sleep(1)

for t in range(10000):

    env.render()
    time.sleep(0.01)

    cart_pos , cart_vel , pole_ang , ang_vel = observation


#    probabilties = model.predict(observation.reshape(1,4))
    probabilties = model.model.predict(observation.reshape(1,4))

    if probabilties[0][0] < probabilties[0][1]:
        action = 1
    else:
        action = 0
    print(t)
    # Perform Action
    observation , reward, done, info = env.step(action)

    if done:
        break
