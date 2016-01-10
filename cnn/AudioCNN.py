import numpy as np
import theano
import theano.tensor as T
import lasagne
import os
import glob
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
             ('conv1', lasagne.layers.Conv2DLayer),
             ('pool1', lasagne.layers.MaxPool2DLayer),
             ('hidden1', lasagne.layers.DenseLayer),
             ('output', lasagne.layers.DenseLayer),
             ],

        # layers parameters
        input_shape=(None, 2, 256, 768),
        conv1_num_filters=64, conv1_filter_size=(256,5),
        conv1_nonlinearity=lasagne.nonlinearities.rectify,
        pool1_pool_size=(4,4),
        hidden1_num_units=256,
        hidden1_nonlinearity=lasagne.nonlinearities.rectify,
        output_num_units=4,
        output_nonlinearity=lasagne.nonlinearities.rectify,

        # learning method and parameters
        update=lasagne.updates.nesterov_momentum,
        update_learning_rate=0.0001,
        update_momentum=0.9,

        # miscellaneous
        regression=False,
        max_epochs=20,
        verbose=3,
        train_split=TrainSplit(eval_size=0.2),
    )

    return network


# Loads the audio data sets (training, validation and test) in a dictionary
def loadAudioData():
    # initialise dictionary
    data = {}
    trainingX, trainingY, developmentX, developmentY, testX, testY = AU.buildAudioData()

    # merge training and development data and add to dictionary
    data['X'] = np.append(trainingX, developmentX, axis=0)
    data['Y'] = np.append(trainingY, developmentY, axis=0)

    # add the test data to dictionary
    data['testX'] = testX
    data['testY'] = testY

    return data


# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    predictions = network.predict(inputs)
    print("Predictions: ", Counter(predictions))
    print("Expected: ", Counter(expectedLabels))
    print("Classification report:\n")
    print(classification_report(expectedLabels, predictions))
    print("Confusion matrix:\n")
    print(confusion_matrix(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))


# takes an path to the audio file and a network and returns an array containing
# the number of times it predicted each label for the different chunks
def evaluate(audioFilePath, network):
    # extract the audio data for the current file
    audioData = AU.extractAudioData(audioFilePath)
    # split the audio data into arrays of size SIZE_CHUNKS
    splitArray = AU.splitData(audioData, AU.SIZE_CHUNKS)
    # predict using the network
    predictions = network.predict(splitArray);
    return dict(Counter(predictions))


def main():
    data = loadAudioData()

    print "Building the network..."
    network = buildCNN()

    print "Training the network..."
    network.fit(data['X'], data['Y'])

    print("Saving the network...")
    utils.saveNet('audioCNN9.pickle', network)

    print "Testing the network with test set..."
    testCNN(network, data['testX'], data['testY'])


if __name__ == '__main__':
    main()
