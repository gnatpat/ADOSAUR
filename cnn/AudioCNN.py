import numpy as np
import theano
import theano.tensor as T
import lasagne
import time
from utils import AudioUtils as AU
from utils import Utils as utils
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import TrainSplit
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from collections import Counter

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

        input_shape=(None, 1, 40000),
        conv1_num_filters=5, conv1_filter_size=3, pool1_pool_size=2,
        hidden1_num_units=50,
        hidden1_nonlinearity=lasagne.nonlinearities.sigmoid,
        output_num_units=64,
        output_nonlinearity=lasagne.nonlinearities.sigmoid,

        # learning parameters
        update_learning_rate=0.0001,
        update_momentum=0.9,

        # miscellaneous
        regression=False,
        max_epochs=5,
        verbose=2,
    )

    return network


# Loads the audio data sets (training, validation and test) in a dictionary
def loadAudioData():
    # initialise dictionary
    data = {}
    trainingX, trainingY, developmentX, developmentY, testX, testY = AU.buildAudioData('../rawData/RawAudio/wav/')

    # merge training and development data and add to dictionary
    data['X'] = np.append(trainingX, developmentX, axis=0)
    data['Y'] = np.append(trainingY, developmentY)

    # add the test data to dictionary
    data['testX'] = testX
    data['testY'] = testY

    return data


def trainCNN(data, save=True, load=False):
    # get our data
    X = data['X']
    Y = data['Y']

    if load:
        # load a pretrained network
        print("Loading the network...")
        network = utils.loadNet('audioCNN.pickle')
    else:
        # build network architecture
        network = buildCNN()
        # train the network
        network.fit(X, Y)

        if save:
            # pickle the network
            print("Saving the network...")
            utils.saveNet('audioCNN.pickle', network)

    return network


# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    predictions = network.predict(inputs)
    print ("Predictions: ", Counter(predictions))
    print ("Expected: ", Counter(expectedLabels))
    # print(classification_report(expectedLabels, predictions))
    # print(confusion_matrix(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))


def main():
    data = loadAudioData()

    print "Building the network..."
    network = buildCNN()

    print "Training the network..."
    network.fit(data['X'], data['Y'])

    print("Saving the network...")
    utils.saveNet('audioCNN.pickle', network)

    # print("Loading the network...")
    # network = utils.loadNet('audioCNN.pickle')

    print "Testing the network with test set..."
    testCNN(network, data['testX'], data['testY'])


if __name__ == '__main__':
    main()
