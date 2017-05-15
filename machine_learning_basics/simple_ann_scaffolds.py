import os

import tensorflow as tf

# initialize variables/model parameters

# define the training loop operations
def inference(X):
    # compute inference model over data X and return the result
    pass

def loss(X, Y):
    # compute loss over training data X and expected outputs Y
    pass

def inputs():
    # read/generate input training data X and expected outputs Y
    pass

def train(total_loss):
    # train / adjust model parameters according to computed total loss
    pass

def evaluate(sess, X, Y):
    # evaluate the resulting trained model
    pass

saver = tf.train.Saver()

# Launch the graph in a session, setup boilerplate
with tf.Session() as sess:

    tf.global_variables_initializer().run()

    X, Y = inputs()

    total_loss = loss(X, Y)
    train_op = train(total_loss)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)


    initial_step = 0

    # verify if we don't have a checkpoint saved already
    ckpt = tf.train.get_checkpoint_state(os.path.dirname(__file__))
    if ckpt and ckpt.model_checkpoint_path:
        # Restores from checkpoint
        saver.restore(sess, ckpt.model_checkpoint_path)
        initial_step = int(ckpt.model_checkpoint_path.rsplit('-', 1)[1])

    # actual training loop
    training_steps = 1000
    for step in range(training_steps):
        sess.run([train_op])
        # for debugging and learning purposes, see how the loss gets decremented thru training steps
        if step % 10 == 0:
            print "loss: ", sess.run([total_loss])

        if step % 1000 == 0:
            saver.save(sess, 'my-model', global_step=step)


        evaluate(sess, X, Y)

    coord.request_stop()
    coord.join(threads)

    saver.save(sess, 'my-model', global_step=training_steps)
    sess.close()