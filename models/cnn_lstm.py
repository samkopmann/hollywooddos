from tensorflow import keras
from keras.layers import Dense,  Conv2D, Flatten, MaxPooling2D, Dropout, LSTM, TimeDistributed

import tensorflow as tf

def getModel(resolution):
  model = keras.Sequential()
  model.add(
      TimeDistributed(Conv2D(
          filters=32,
          kernel_size=3,
          activation='relu',
          input_shape=(resolution, resolution, 1)
      ))
  )
  model.add(
      TimeDistributed(Conv2D(
          filters=32,
          kernel_size=3,
          activation='relu',
      ))
  )
  model.add(TimeDistributed(MaxPooling2D(pool_size=2)))
  model.add(TimeDistributed(Dropout(0.1)))
  model.add(
      TimeDistributed(Conv2D(
          filters=32,
          kernel_size=3,
          activation='relu',
      ))
  )
  model.add(
      TimeDistributed(Conv2D(
          filters=32,
          kernel_size=3,
          activation='relu',
      ))
  )
  model.add(TimeDistributed(MaxPooling2D(pool_size=2)))
  model.add(TimeDistributed(Dropout(0.1)))
  model.add(TimeDistributed(Flatten()))
  model.add(
      TimeDistributed(Dense(64,activation="relu"))
  )
  model.add(LSTM(64, return_sequences=False))
  model.add(Dense(32, activation='relu'))
  model.add(Dense(1, activation='sigmoid'))

  model.compile(
      loss='binary_crossentropy',
      metrics=['accuracy', 
      tf.keras.metrics.Precision(name="precision"),
      tf.keras.metrics.Recall(name="recall"),
      tf.keras.metrics.FalsePositives(name="FP"),
      tf.keras.metrics.FalseNegatives(name="FN")
      ]
  )
  return model