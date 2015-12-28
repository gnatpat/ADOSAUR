import numpy as np
import theano
import theano.tensor as T
import lasagne
import time
from utils import LoadData as LD
from utils import AudioDataFormatter as ADF
from utils import Utils as utils
from nolearn.lasagne import NeuralNet

def buildCNN(inputVar=None):

    network = NeuralNet(
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
        output_num_units = 64,  # 64 target values for the digits 0, 1, 2, ..., 63

        # optimization method
        update = lasagne.updates.nesterov_momentum,
        update_learning_rate = 0.01,
        update_momentum = 0.9,

        regression = False,
        max_epochs = 5,
        verbose = 1,
    )

    return network


def loadAudioData():
    data = {}  # initialise dictionary
    trainingX, trainingY, developmentX, developmentY, testX, testY = ADF.buildAudioData('../rawData/RawAudio/wav/')
    data['trainingX'] = trainingX
    data['trainingY'] = trainingY
    data['developmentX'] = developmentX
    data['developmentY'] = developmentY
    data['testX'] = testX
    data['testY'] = testY

    return data


def trainCNN(data, save=True, load=False):
    # get our data
    trainingX = data['trainingX']
    trainingY = data['trainingY']

    if load:
        # load a pretrained network
        network = utils.loadNet('audioCNN.pickle')
    else:
        # build network architecture
        network = buildCNN()

    # train the network
    network.fit(trainingX, trainingY)

    if save:
        # pickle the network
        utils.saveNet('audioCNN.pickle', network)

    return network


def predictInput(example, network):
    return network.predict(example)


def main():
    # load our data
    data = loadAudioData()
    # train the cnn
    network = trainCNN(data, False, False)
    # make a prediction
    print("\nActual:\t\t%s" % str(data['trainingY'][0]))
    print("Predicted:\t%s" % str(predictInput([data['trainingX'][0]], network)))

if __name__ == '__main__':
    main()
