import tensorflow as tf
import gym,time


#############################################
### RUN TRAINED MODEL ON ENVIRONMENT #######
###########################################


env = gym.make('CartPole-v0')

num_inputs = 4
num_hidden = 4
num_outputs = 1
learning_rate = 0.01

initializer = tf.contrib.layers.variance_scaling_initializer()
X = tf.placeholder(tf.float32, shape=[None, num_inputs])
hidden_layer_one = tf.layers.dense(X, num_hidden, activation=tf.nn.relu, kernel_initializer=initializer)
hidden_layer = tf.layers.dense(hidden_layer_one, num_hidden, activation=tf.nn.relu, kernel_initializer=initializer)
logits = tf.layers.dense(hidden_layer, num_outputs)
outputs = tf.nn.sigmoid(logits)  # probability of action 0 (left)

probabilties = tf.concat(axis=1, values=[outputs, 1 - outputs])
action = tf.multinomial( probabilties, num_samples=1)
# Convert from Tensor to number for network training
y = 1. - tf.to_float(action)

########################################
### LOSS FUNCTION AND OPTIMIZATION ####
######################################
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(labels=y, logits=logits)
optimizer = tf.train.AdamOptimizer(learning_rate)

# https://stackoverflow.com/questions/41954198/optimizer-compute-gradients-how-the-gradients-are-calculated-programatically
# https://www.tensorflow.org/api_docs/python/tf/train/AdamOptimizer


################################
#### GRADIENTS ################
##############################
gradients_and_variables = optimizer.compute_gradients(cross_entropy)



gradients = []
gradient_placeholders = []
grads_and_vars_feed = []

for gradient, variable in gradients_and_variables:
    gradients.append(gradient)
    gradient_placeholder = tf.placeholder(tf.float32, shape=gradient.get_shape())
    gradient_placeholders.append(gradient_placeholder)
    grads_and_vars_feed.append((gradient_placeholder, variable))



observations = env.reset()
with tf.Session() as sess:
    # https://www.tensorflow.org/api_guides/python/meta_graph
    new_saver = tf.train.import_meta_graph('./models/my-650-step-model.meta')
    new_saver.restore(sess,'./models/my-650-step-model')

    for x in range(500):
        env.render()
        time.sleep(0.01)
        action_val, gradients_val = sess.run([action, gradients], feed_dict={X: observations.reshape(1, num_inputs)})
        observations, reward, done, info = env.step(action_val[0][0])