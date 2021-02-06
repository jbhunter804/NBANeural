#!/bin/python
import os
import time
import warnings
import numpy as np
import keras
import tensorflow as tf
import random
import csv
from numpy import newaxis
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import BatchNormalization
from keras.models import Sequential, load_model
from keras.utils import plot_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt

def standardizeInputs(data):
    # create scaler
    scaler = StandardScaler()
    # fit scaler on data
    scaler.fit(data)
    # apply transform
    standardized = scaler.transform(data)
    return standardized

def stripQuotes(data):
    answer = []
    for entry in data:
#         print(entry)
        curRow = []
        for i in range(len(entry)):
#             print(entry[i])
            curEntry = entry[i].replace("\"","")
            curRow.append(curEntry)
        answer.append(curRow)
    answer = np.array(answer)
    return answer

def createXYImpliedProbs(data):
    try:
        XY, ImpliedProbs = np.split(data,[-2],axis=1)

        gIY, ScoreX = np.split(XY,[2],axis=1)
        Score, X = np.split(ScoreX,[2],axis=1)
        gameIDs, Y = np.split(gIY,[1],axis=1)
    except:
        XY, ImpliedProbs = np.split(data,[-2],axis=0)
        gIY, ScoreX = np.split(XY,[2],axis=0)
        Score, X = np.split(ScoreX,[2],axis=0)
        gameIDs, Y = np.split(gIY,[1],axis=0)
#     print(X[0])
    return X, Y, ImpliedProbs, gameIDs

def build_model(layers, batch_size, modelWeightFile, dropRate=0.5, loadModel = 1,learning_rate = 0.1, decay_rate = 0.005, epochs=100):
    model = Sequential()
    startWeights = keras.initializers.RandomNormal(mean=0, stddev=(1/100)**0.5, seed=-1)
    totalLayers = len(layers)
    model.add(Dense(layers[0], input_shape=(layers[0],), kernel_initializer=(startWeights)))
    model.add(BatchNormalization())
    model.add(Dropout(dropRate))
    for i in range(1,totalLayers-1):
        stddev = (1/layers[i-1])**0.5
        model.add(Dense(layers[i], activation='relu', kernel_initializer= keras.initializers.RandomNormal(mean=0, stddev=stddev, seed=-1)))
        model.add(BatchNormalization())
        model.add(Dropout(dropRate))
    model.add(Dense(layers[-1], activation='relu'))
    model.add(Dense(1, activation='sigmoid' )) # linear for spread, sigmoid for win/loss
    if loadModel > 0:
        model.load_weights(modelWeightFile)
    start = time.time()
	# model.compile(loss="mse", optimizer="adam") #for spread
    decay_steps = 1.0# inFileData = "gameData" + date.strftime('%Y-%m-%d') + ".csv"

    decay_rate = decay_rate
    learning_rate_fn = keras.optimizers.schedules.InverseTimeDecay(learning_rate, decay_steps, decay_rate)
    model.compile(loss="binary_crossentropy", optimizer="adam") #for win/loss
    print("> Compilation Time : ", time.time() - start)
    return model




date = datetime.today() - timedelta(hours=14, minutes=00)
inFileData = "nextDataForModel.csv"
newData = np.loadtxt(open(inFileData, "r"),dtype=np.unicode_, delimiter=",")
inFileTrainData = "modelDevData.csv"
allData = np.loadtxt(open(inFileTrainData, "r"),dtype=np.unicode_, delimiter=",")
# print(allData.shape)
newObservations = 1
try:
    _ = newData.shape[1]
    newObservations = newData.shape[0]
    print(newObservations)
except:
    print("only 1 observation")

dataStripped = stripQuotes(allData)
X_str, Y_str, ImpliedProbs_str, homeIDs = createXYImpliedProbs(dataStripped)

X = X_str.astype(np.float)
X = standardizeInputs(X)
Y = Y_str.astype(np.float)
ImpliedProbs = ImpliedProbs_str.astype(np.float)
X = np.concatenate((X,ImpliedProbs), axis=1)

epochs = 0
batch_size = 256
drop_rate = 0.64
learning_rate  = 0.24
decay_rate = 0.0025
modelWeightFile1 = "modelWeights26.h5"
model = build_model([1408, 500, 240, 60, 25, 13, 1], batch_size, modelWeightFile1, dropRate= drop_rate, loadModel=1, learning_rate = learning_rate, decay_rate = decay_rate,epochs= epochs)


predictions = model.predict(X, batch_size=batch_size, verbose=0)
predictionFile = "todayPreds.csv"
predFile = open(predictionFile, "w")

writer = csv.writer(predFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
predictionLen = len(predictions)
combinedMatrix = []
# for i in range(newObservations):
for i in range(newObservations):
	row = []
	homeID = homeIDs[-(i+1)][0]
	row.append(homeID)
	row.append(predictions[-(i+1)][0])
	writer.writerow(row)
predFile.close()


