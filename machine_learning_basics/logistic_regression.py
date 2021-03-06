import os

import tensorflow as tf

# initialize variables/model parameters
W = tf.Variable(tf.zeros([5, 1]), name="weights")
b = tf.Variable(0., name="bias")

def read_csv(batch_size, file_name, record_defaults):
    filename_queue = tf.train.string_input_producer([os.path.dirname(__file__) + "/" + file_name])

    reader = tf.TextLineReader(skip_header_lines=1)
    key, value = reader.read(filename_queue)

    # decode_csv will convert a Tensor from type string (the text line) in
    # a tuple of tensor columns with the specified defaults, which also
    # sets the data type for each column
    decoded = tf.decode_csv(value, record_defaults=record_defaults)

    # batch actually reads the file and loads "batch_size" rows in a single tensor
    return tf.train.shuffle_batch(decoded,
                                  batch_size=batch_size,
                                  capacity=batch_size * 50,
                                  min_after_dequeue=batch_size)


# former inference is now used for combining inputs
def combine_inputs(X):
    return tf.matmul(X, W) + b

# define the training loop operations
def inference(X):
    # compute inference model over data X and return the result
    return tf.sigmoid(combine_inputs(X))

def loss(X, Y):
    # compute loss over training data X and expected outputs Y
    # Y_predicted = inference(X)
    # return tf.reduce_sum(tf.squared_difference(Y, Y_predicted))
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=combine_inputs(X), labels=Y))




def inputs():
    # read/generate input training data X and expected outputs Y
    passenger_id, survived, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked = \
        read_csv(100, "titanic_survivor_kaggle/train.csv", [[0.0], [0.0], [0], [""], [""], [0.0], [0.0], [0.0], [""], [0.0], [""], [""]])

    # convert categorical data
    is_first_class = tf.to_float(tf.equal(pclass, [1]))
    is_second_class = tf.to_float(tf.equal(pclass, [2]))
    is_third_class = tf.to_float(tf.equal(pclass, [3]))

    gender = tf.to_float(tf.equal(sex, ["female"]))

    # Finally we pack all the features in a single matrix;
    # We then transpose to have a matrix with one example per row and one feature per column.
    features = tf.transpose(tf.stack([is_first_class, is_second_class, is_third_class, gender, age]))
    survived = tf.reshape(survived, [100, 1])

    return features, survived

def train(total_loss):
    # train / adjust model parameters according to computed total loss
    learning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(total_loss)


def evaluate(sess, X, Y):
    # evaluate the resulting trained model
    predicted = tf.cast(inference(X) > 0.5, tf.float32)
    print "Accuracy: ", sess.run(tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32)))


saver = tf.train.Saver()
model_name = 'logist_regression'

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
    # ckpt = tf.train.get_checkpoint_state(os.path.dirname(__file__))
    # if ckpt and ckpt.model_checkpoint_path:
    #     # Restores from checkpoint
    #     saver.restore(sess, ckpt.model_checkpoint_path)
    #     initial_step = int(ckpt.model_checkpoint_path.rsplit('-', 1)[1])

    # actual training loop
    training_steps = 300
    for step in range(training_steps):
        sess.run([train_op])
        # for debugging and learning purposes, see how the loss gets decremented thru training steps
        if step % 10 == 0:
            print "loss: ", sess.run([total_loss])

        if step % 100 == 0:
            saver.save(sess, model_name, global_step=step)

    evaluate(sess, X, Y)

    coord.request_stop()
    coord.join(threads)

    saver.save(sess, model_name, global_step=training_steps)
    sess.close()
