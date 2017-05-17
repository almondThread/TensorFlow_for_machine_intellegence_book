import tensorflow as tf

# The match_filenames_once will accept a regex but there is no need for this example.
image_filename = "./test-input-image.jpg"
filename_queue = tf.train.string_input_producer(tf.train.match_filenames_once(image_filename))

image_reader = tf.WholeFileReader()
_, image_file = image_reader.read(filename_queue)
# image = tf.image.decode_jpeg(image_file)


with tf.Session() as sess:
    tf.global_variables_initializer().run()

    # sess.run(image_reader)
    print image_filename
    sess.run(image_file)

    # # Coordinate the loading of image files.
    # coord = tf.train.Coordinator()
    # threads = tf.train.start_queue_runners(coord=coord)

    # Get an image tensor and print its value.
    # image_tensor = sess.run([image])
    # print(image_tensor)