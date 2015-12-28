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

        # TODO: need to change regression to False
        regression = False,
        max_epochs = 1,
        verbose = 1,
    )

    return network


def trainCNN(save=True, load=False):
    # load our data
    trainingX, trainingY, developmentX, developmentY, testX, testY = ADF.buildAudioData('../rawData/RawAudio/wav/')

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

def main():
    trainCNN(True, False)

if __name__ == '__main__':
    main()
