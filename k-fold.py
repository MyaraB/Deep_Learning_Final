# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aWsNxYJrsHWHsPOEIdzARdGeix07CXkU
"""

from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import RMSprop
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

url = Path('/content/drive/MyDrive/למידה עמוקה מטלת גמר/Diamonds/data_.csv')
df1 = pd.read_csv(url)
df = pd.DataFrame(df1)
df = df.astype('float32')
df=df.to_numpy()

np.random.shuffle(df)

data_x = np.array(df[:,[0,1,2,3,4,5,6,7,8,9,10]])
data_y = np.array(df[:,-1])

data_y=data_y


x_train,x_test,y_train,y_test = train_test_split(data_x,data_y,test_size=0.3,random_state=142)

X_train= np.array(x_train)
X_test = np.array(x_test)
y_train = np.array(y_train).reshape((-1,1))
y_test = np.array(y_test).reshape((-1,1))


# define base model
def baseline_model():
    # create model
    model = Sequential()
    # add 1st layer
    model.add(Dense(18, input_dim=11, activation='relu')) 
    # kernel_initializer='normal',
    # add hidden layer
    model.add(Dense(12, kernel_initializer='normal', activation='relu'))
    # add output layer
    model.add(Dense(1, kernel_initializer='normal'))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=10)
kf = KFold(n_splits=5)
results = cross_val_score(estimator, X_train, y_train, cv=kf)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


estimator.fit(X_train, y_train)
y_pred = estimator.predict(X_test)# Plot a scatter plot like above to see predictio
plt.scatter(y_test,y_pred)

predicted_price = np.squeeze(baseline_model().predict(X_test))
true_price = y_test