import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import datetime
import json
import numpy as np

from models import cnn_lstm
from data.preprocessing import file_descriptor

config = {}
# Read json file
with open('training_parameters.json') as json_file:
    config = json.load(json_file)

histories = {}
time = datetime.datetime.now().strftime("%Y%m%d-%H:%M")
result_file = '../results/training/%s.json' % time


for resolution in config['resolution']:
    histories[resolution] = {}
    for window_size in config["window_size"]:
        histories[resolution][window_size] = {}
        for scale in config["scale"]:
            histories[resolution][window_size][scale] = {}
            training_data_file_name = file_descriptor.getTrainingDataFileName(resolution, window_size, scale)
            dataset = pd.read_csv("../data/training/%s"%(training_data_file_name), delimiter=",", header=None, 
                 index_col=False)
            for series_length in config['series_length']:
                histories[resolution][window_size][scale][series_length] = []
                for run in range(config["runs"]):
                    #Hash string to be used as filename
                    dataset=dataset.values

                    X_train = dataset[:,1:-2]
                    number = X_train.shape[0]

                    X_train = X_train.reshape(number, resolution, resolution, 1).astype('float32')
                    Y_train = dataset[:,-1:]
                    training_set = []
                    training_labels = []

                
                    for i in range(series_length, X_train.shape[0], 1):
                        c = np.array(X_train[i-series_length:i])
                        mean = np.mean(c)
                        std = np.std(c)
                        c = (c-mean)/std

                        training_set.append(c)
                        training_labels.append(Y_train[i])

                    X = np.array(training_set)
                    Y = np.array(training_labels)

                    X,Y = shuffle(X,Y)

                    model = cnn_lstm.getModel(resolution)
                    history = model.fit(X,Y,epochs=config["epochs"], validation_split=config["validation_split"], batch_size=200, verbose=1)
                    histories[resolution][window_size][scale][series_length].append({
                        "accuracy": history.history["accuracy"],
                        "val_accuracy": history.history["val_accuracy"],
                        "val_TP": history.history["val_TP"],
                        "val_TN": history.history["val_TN"],
                        "val_FP": history.history["val_FP"],
                        "val_FN": history.history["val_FN"],
                    })
                json_string = json.dumps(histories)
                with open(result_file, 'w') as outfile:
                    json.dump(json_string, outfile)