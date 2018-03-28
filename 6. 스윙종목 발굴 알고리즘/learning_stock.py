import pandas as pd
import openpyxl
import random
import re
import numpy as np
from sklearn import model_selection, svm, metrics
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier
from sklearn.naive_bayes import GaussianNB
import pickle
from sklearn.neural_network import MLPClassifier
from keras.models import Sequential
from keras.layers.core import Dropout, Dense, Activation
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, Callback
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score



with open('data.p', 'rb') as file:    # hello.txt 파일을 바이너리 읽기 모드(rb)로 열기
    train_X = pickle.load(file)
    train_y = pickle.load(file)
    test_X = pickle.load(file)
    test_y = pickle.load(file)

#for index, val in enumerate(train_y) :                   #label이 1인 자료들을 더 추가
#    if val == 1 :
#        train_X.append(train_X[index])
#        train_y.append(1)
#    if index > 4000 :
#        break

#for index, val in enumerate(test_y) :
#    if val == 1 :
#        test_X.append(test_X[index])
#        test_y.append(1)
#    if index > 2000 :
#        break

train_X = np.array(train_X)
test_X = np.array(test_X)
#test_X = np.array(test_X[2000:])
train_y = np_utils.to_categorical(np.array(train_y))
test_y = np_utils.to_categorical(np.array(test_y))
#test_y = np_utils.to_categorical(np.array(test_y[2000:]))




model = Sequential()


model.add(Dense(1000, input_shape=(80,)))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(1000))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(1000))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(2))

model.add(Activation('softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='rmsprop',
    metrics=['accuracy'])
# 데이터 훈련하기 --- (※5)
hist = model.fit(train_X, train_y, batch_size=100, nb_epoch=20, validation_split=0.1, callbacks=[EarlyStopping(monitor='val_loss', patience=2)], verbose=1)
# 테스트 데이터로 평가하기 --- (※6)
score = model.evaluate(test_X, test_y, verbose=1)
print('loss=', score[0])
print('accuracy=', score[1])