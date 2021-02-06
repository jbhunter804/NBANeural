import os
import time
import warnings
import numpy as np
# import keras
import tensorflow as tf
from tensorflow import keras
import random
from numpy import newaxis
from tensorflow.keras.layers.core import Dense, Activation, Dropout
from tensorflow.keras.layers.recurrent import LSTM
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #Hide messy TensorFlow warnings
warnings.filterwarnings("ignore") #Hide messy Numpy warnings

trainData = read_csv("modelTrainData.csv")
devData = read_csv("modelDevData.csv")
testData = read_csv("modelTestData.csv")