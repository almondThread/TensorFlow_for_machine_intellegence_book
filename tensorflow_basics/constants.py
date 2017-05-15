import tensorflow as tf

a = tf.constant(5, name="input_a")
b = tf.constant(3, name="input_b")
c = tf.multiply(a,b, name="mul_c")
d = tf.add(a,b, name="add_d")
e = tf.add(c,d, name="add_e")

sess = tf.Session()

# run in terminal 'tensorboard --logdir="./graphs/"'
writer = tf.summary.FileWriter('./graphs', sess.graph)

sess.run(e)

writer.close()
sess.close()