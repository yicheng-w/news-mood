import tensorflow as tf
from pre_processing import *

EPOCH_COUNT = 200

ALPHA = 0.05
INPUT_SZ = 18 # headline at max 18 words
OUTPUT_SZ = 6 # 6 output emotions

input = tf.placeholder(tf.float32, [None, INPUT_SZ])
output = tf.placeholder(tf.float32, [None, OUTPUT_SZ])

W = tf.Variable(tf.random_normal([INPUT_SZ, OUTPUT_SZ], 0.5, 0.25))
b = tf.Variable(tf.random_normal([OUTPUT_SZ], 0.5, 0.25))

yp = tf.nn.softmax(tf.matmul(input, W) + b)

loss = tf.reduce_mean(-tf.reduce_sum(output * tf.log(yp), reduction_indices=[1]))

train_fn = tf.train.AdamOptimizer().minimize(loss)

correct = tf.equal(tf.argmax(yp, 1), tf.argmax(output, 1))
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

session = tf.Session()

session.run(tf.global_variables_initializer())

set_train_file_loc("../emotion_data_train.csv")

xt, yt = read_test("../emotion_data_test.csv")

for i in xrange(EPOCH_COUNT):
    x, y = get_batch(100)
    session.run([loss, train_fn], {
        input: x, output: y
        })

    print session.run(accuracy, {input: xt, output: yt})
