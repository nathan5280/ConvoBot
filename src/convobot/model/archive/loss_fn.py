import numpy as np

import os
# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# Launch the graph in a session.
sess = tf.Session()

if False:
    # Build a graph.
    a = tf.constant(5.0)
    b = tf.constant(6.0)
    c = a * b

    # Evaluate the tensor `c`.
    print(sess.run(c))

if False:
    d = np.array([45, -5, 370])
    print(d)
    sq = tf.map_fn(lambda x: x*x, d)
    # sq = tf.Print(sq, [sq])
    x = sess.run(sq)
    print(x)

def adj_theta(t):
    print('adj_theta')
    print(type(t))
    print(t)

    if t > 360:
        return t-360
    elif t < 0:
        return t+360
    else:
        return t

d = np.array([45, -5, 370])
a = tf.map_fn(lambda x: adj_theta(x), d)
x = sess.run(a)
print(x)


# adj = tf.map_fn(lambda x: adj_theta(x), d)
