import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.utils import np_utils
from keras.optimizers import RMSprop
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import math
from sklearn.metrics import mean_squared_error

look_back = 1


def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        dataX.append(a)
        if dataset[i + look_back+1] > dataset[i + look_back] :
            dataY.append(1)
        else :
            dataY.append(0)
    return np.array(dataX), np.array(dataY)


pandf = pd.read_csv("KOSPI.csv", index_col="date")




# convert nparray
nparr = pandf['index'].values[::-1]


nparr = nparr.astype('float32').reshape(-1,1)



# normalization
scaler = MinMaxScaler(feature_range=(0, 1))
nptf = scaler.fit_transform(nparr)


# split train, test
train_size = int(len(nptf) * 0.9)
test_size = len(nptf) - train_size
train, test = nptf[0:train_size], nptf[train_size:len(nptf)]
print(len(train), len(test))

# create dataset for learning
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)
trainY = np_utils.to_categorical(trainY)
testY = np_utils.to_categorical(testY)
print(trainX, trainY)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

# simple lstm network learning   Acrivation을 쓰면 결과가 안나오더라.
model = Sequential()
model.add(LSTM(4, input_shape=(1, look_back)))
model.add(Dense(20))
model.add(Activation('relu'))
model.add(Dense(2))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(trainX, trainY, epochs=200, batch_size=14, verbose=2)

score = model.evaluate(testX, testY)

print("loss=",score[0])
print("accuracy=",score[1])

# make prediction
testPredict = model.predict(testX)


# predict last value (or tomorrow?)
lastX = nptf[-1]


lastX = np.reshape(lastX, (1, 1, 1))
lastY = model.predict(lastX)

print(lastY)


