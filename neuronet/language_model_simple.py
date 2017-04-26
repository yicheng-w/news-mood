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

    ypp = session.run(yp, {input: xt})

    correct = 0
    total = yt.shape[0]
    for i in xrange(yt.shape[0]):
        acceptable_vals = []
        for j in xrange(yt.shape[1]):
            if yt[i, j] > 0:
                acceptable_vals.append(j)
        acceptable_vals = sorted(acceptable_vals, reverse=True,
                key=lambda x: yt[i, x])[:3]

        #print yt[i, :]
        #print acceptable_vals

        max_p = -1
        max_i = -1
        for j in xrange(yt.shape[1]):
            if ypp[i, j] > max_p:
                max_p = ypp[i, j]
                max_i = j

        if max_i in acceptable_vals:
            correct += 1

    print(float(correct) / total)
    print(session.run(accuracy, {input: xt, output: yt}))
    print("===")
