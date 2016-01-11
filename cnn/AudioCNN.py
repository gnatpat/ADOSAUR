import numpy as np
import theano
import theano.tensor as T
import lasagne
import os
import glob
import random
from utils import AudioUtils as AU
from utils import Utils as utils
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import TrainSplit
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from collections import Counter

# prevent error when pickling large network
import sys
sys.setrecursionlimit(10000)

# Builds the network
def buildCNN():

    network = NeuralNet(
        # specify the layers
        layers=[
             ('input', lasagne.layers.InputLayer),
             ('conv1', lasagne.layers.Conv1DLayer),
             ('pool1', lasagne.layers.MaxPool1DLayer),
             ('hidden1', lasagne.layers.DenseLayer),
             ('output', lasagne.layers.DenseLayer),
             ],

        # layers parameters
        input_shape=(None, 1, AU.SIZE_CHUNKS),
        conv1_num_filters=5, conv1_filter_size=3,
        pool1_pool_size=2,
        hidden1_num_units=1000,
        hidden1_nonlinearity=lasagne.nonlinearities.sigmoid,
        output_num_units=4,
        output_nonlinearity=lasagne.nonlinearities.sigmoid,

        # learning method and parameters
        update=lasagne.updates.nesterov_momentum,
        update_learning_rate=0.0001,
        # update_momentum=0.9,

        # miscellaneous
        regression=False,
        max_epochs=1500,
        verbose=1,
        train_split=TrainSplit(eval_size=0.2),
    )

    return network


# Loads the audio data sets (training, validation and test) in a dictionary
def loadData():
    # initialise dictionary
    data = {}
    # build the audio data and augment it
    trainingX, trainingY, developmentX, developmentY, testX, testY = AU.buildAudioData()
    trainingX, trainingY, developmentX, developmentY = AU.augmentData(trainingX, trainingY, developmentX, developmentY)

    # merge training and development data and add to dictionary
    data['X'] = np.append(trainingX, developmentX, axis=0)
    data['Y'] = np.append(trainingY, developmentY)

    # add the test data to dictionary
    data['testX'] = testX
    data['testY'] = testY

    return data


def main():
    data = loadData()

    print "Building the network..."
    network = buildCNN()

    print "Training the network..."
    network.fit(data['X'], data['Y'])

    print("Saving the network...")
    utils.saveNet('audioCNN.pickle', network)

    # print ("Loading the network...")
    # network = utils.loadNet('audioCNN10.pickle')

    print "Testing the network with test set..."
    utils.testCNN(network, data['testX'], data['testY'])


if __name__ == '__main__':
    main()
