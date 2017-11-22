#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import tensorflow as tf
import random
import numpy as np


# 1.训练的数据
# Make up some real data
# tmp = random.randint(0, 100)
x_data = np.float32(np.random.rand(1,2))
# y_data = np.dot([0.1, 0.2], x_data) + 0.3
# x_data = random.randint(0, 100)
y_data = x_data * 2 + 3


b = tf.Variable(tf.zeros([1]))
w = tf.Variable(tf.random_normal([1, 1], 1.0, 4.0))
y = tf.matmul(w, x_data) + b

loss = tf.reduce_mean(tf.square(y - y_data ))
op = tf.train.GradientDescentOptimizer(0.1)
train = op.minimize(loss)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

for step in range(1000):
    sess.run(train)
    if step % 50 == 0:
        print(step, sess.run(loss), sess.run(w), sess.run(b))