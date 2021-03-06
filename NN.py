# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aWsNxYJrsHWHsPOEIdzARdGeix07CXkU
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import csv
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

#load the data set + convert it to type numpy compatible with tensorflow
url = Path('/content/drive/MyDrive/למידה עמוקה מטלת גמר/Diamonds/data_.csv')
df1 = pd.read_csv(url)
df = pd.DataFrame(df1)
df = df.astype('float32')
df=df.to_numpy()

#shuffle data
np.random.shuffle(df)

data_x = np.array(df[:,[0,1,2,3,4,5,6,7,8,9,10]])
data_y = np.array(df[:,-1])

data_y=data_y


x_train,x_test,y_train,y_test = train_test_split(data_x,data_y,test_size=0.3,random_state=0)

#shaping the data in-order for it to be usable with tensor
data_x = np.array(x_train)
test_x = np.array(x_test)
data_y = np.array(y_train).reshape((-1,1))
test_y = np.array(y_test).reshape((-1,1))

learning_rate = 0.000001
features =11
hidden1_size=132
training_epochs = 140000

#pre proccesing..
x = tf.placeholder(tf.float32, [None, features])
y_ = tf.placeholder(tf.float32, [None, 1])
W1 = tf.Variable(tf.truncated_normal([features, hidden1_size], stddev=0.1))
b1 = tf.Variable(tf.constant(0.1, shape=[hidden1_size]))
z1 = tf.nn.relu(tf.matmul(x,W1)+b1)
W2 = tf.Variable(tf.truncated_normal([hidden1_size, 1], stddev=0.1))
b2 = tf.Variable(tf.constant(0.1, shape=[1]))

#y = tf.nn.sigmoid(tf.matmul(z1,W2)+b2)
y = tf.matmul(z1,W2)+b2

loss = tf.reduce_mean(tf.pow(y-y_,2))
update = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

#loss=tf.reduce_mean(-(y_*tf.log(y + eps) + (1 - y_+eps)*tf.log(1 - y+eps)))
#update = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

prediction = tf.round(tf.sigmoid(tf.matmul(z1,W2)+b2))
correct = tf.cast(tf.equal(prediction, y_), dtype=tf.float32) 
accuracy = tf.reduce_mean(tf.cast(correct,tf.float32))

sess = tf.Session()
sess.run(tf.global_variables_initializer())
for epoch in range(0,training_epochs+1):
  sess.run(update, feed_dict = {x:data_x, y_:data_y})
  if (epoch+1)%1000==0:
    err, _ = sess.run([loss, update], {x: data_x, y_:data_y})
    feeds_train = {x:data_x, y_:data_y}
    feeds_test = {x:test_x, y_:test_y}
    train_acc = sess.run(accuracy, feed_dict=feeds_train)
    test_acc = sess.run(accuracy, feed_dict=feeds_test)
    print ("epoch: %3d loss: %.3f" % (epoch+1, err))