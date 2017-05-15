import tensorflow as tf

# Create a new graph:
# g = tf.Graph()
# with g.as_default():
#     # Create Operations as usual; they will be added to graph `g`
#     a = tf.mul(2, 3)
#
# # Placed in the default graph
# in_default_graph = tf.add(1,2)
# default_graph = tf.get_default_graph()


g1 = tf.Graph()
g2 = tf.Graph()

with g1.as_default():
    # Define g1 Operations, tensors, etc.
    tf.mul(2, 3)

with g2.as_default():
    # Define g2 Operations, tensors, etc.
    tf.mul(2, 3)

