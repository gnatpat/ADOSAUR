import numpy as np
import theano
import theano.tensor as T
import lasagne
import time
from utils import AudioUtils as AU
from utils import Utils as utils
from nolearn.lasagne import NeuralNet
from sklearn.metrics import classification_report, accuracy_score


# Builds the network
def buildCNN():

    network = NeuralNet(
        # specify the layers
        layers=[('input', lasagne.layers.InputLayer),
                ('conv1', lasagne.layers.Conv1DLayer),
                ('hidden', lasagne.layers.DenseLayer),
                ('output', lasagne.layers.DenseLayer),
                ],

        # layer parameters
        input_shape = (None, 1, 10000),
        hidden_num_units = 20,  # number of units in 'hidden' layer
        conv1_num_filters = 20, conv1_filter_size = 2,
        output_nonlinearity = lasagne.nonlinearities.softmax,
        output_num_units = 64,  # 64 target values for the depression indices

        # optimization method
        update = lasagne.updates.nesterov_momentum,
        update_learning_rate = 0.01,
        update_momentum = 0.9,

        regression = False, # classification problem
        max_epochs = 3,
        verbose = 1,

        # TODO: needs to be checked that eval_size actually just splits the
        # data in training and validation (50/50 here)
        eval_size = 0.5,
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

    # add them separately in case we need it
    data['trainingX'] = trainingX
    data['trainingY'] = trainingY
    data['developmentX'] = developmentX
    data['developmentY'] = developmentY

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


# Makes a prediction for a single input given a network
def predictSingleInput(example, network):
    return network.predict(example)


# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    # TODO: may need a fix, getting some warnings
    predictions = network.predict(inputs)
    print(classification_report(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))


def main():
    # load our data
    data = loadAudioData()
    # train the cnn
    network = trainCNN(data, False, False)
    # test the cnn
    testCNN(network, data['testX'], data['testY'])


if __name__ == '__main__':
    main()
