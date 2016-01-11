import random

import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import PrintLayerInfo
from nolearn.lasagne import TrainSplit

from nolearn.lasagne.visualize import plot_loss
from nolearn.lasagne.visualize import plot_conv_weights
from nolearn.lasagne.visualize import plot_conv_activity
from nolearn.lasagne.visualize import plot_occlusion

import numpy as np
import pickle

from utils.VideoUtils import getCNNdata
from utils.Utils import testCNN
from utils.Utils import saveNet
from utils.Utils import loadNet

UNITS_ON_BDI = 4


# Loads training, validation and testing data
def loadData():
    # retrieve data
    trainingX, trainingY, validationX, validationY, testingX, testingY = getCNNdata()

    # initialise and populate dictionary
    data = {}
    data['trainingX']   = trainingX    # a list of grayscale images
    data['trainingY']   = trainingY    # a list of ints (on BDI scale)
    data['validationX'] = validationX  # a list of grayscale images
    data['validationY'] = validationY  # a list of ints (on BDI scale)
    data['testingX']    = testingX     # a list of grayscale images
    data['testingY']    = testingY     # a list of ints (on BDI scale)
    data['num_examples_train'] = trainingX.shape[0]
    data['input_shape'] = (None,) + trainingX.shape[1:]
    data['output_dim'] = UNITS_ON_BDI  # BDI scale

    # Report number of training examples found
    print("\n\nGot %i training datasets.\n" % data['num_examples_train'])
    
    return data

def buildCNN(data):
    # small net for proof of concept
    # see http://goo.gl/GZUQOb for more realistic config
    network = NeuralNet(
        # architecture
        layers=[
            ('input', layers.InputLayer),
            (layers.Conv2DLayer, {'num_filters':64, 'filter_size':(3, 3)}),
            (layers.MaxPool2DLayer, {'pool_size': (2, 2)}),
            ('hidden2', layers.DenseLayer),
            ('output', layers.DenseLayer),
            ],
        input_shape=data['input_shape'],
        hidden2_num_units=1000,
        hidden2_nonlinearity=lasagne.nonlinearities.sigmoid,
        output_num_units=data['output_dim'],
        output_nonlinearity=lasagne.nonlinearities.sigmoid,

        # learning parameters
        update_learning_rate=0.0001,
        update_momentum=0.9,
        update=lasagne.updates.nesterov_momentum,

        # miscellaneous
        regression=False,
        max_epochs=500,
        verbose=3,
        train_split=TrainSplit(eval_size=0.2)
    )

    # TODO: pickle trained network (after we've optimised)

    return network

def CNN(data):
    # build network - need data to determine input/output shapes
    print("Building network...")
    network = buildCNN(data)

    # train the network
    print("Training network...\n")
    network.fit(data['trainingX'], data['trainingY'])
    return network

def main():
    data = loadData()

    network = loadNet('videoCNN1.save')
    network.fit(data['trainingX'], data['trainingY'])

    # layer_info = PrintLayerInfo()
    # layer_info(network)

    testCNN(network, data['testingX'], data['testingY'])

    saveNet('videoCNN1.save', network)

    testCNN(network, data['trainingX'], data['trainingY'])

    testCNN(network, data['validationX'], data['validationY'])

    plot_loss(network).show()

    face = random.random() * data['trainingX'].shape[0]

    plot_conv_activity(network.layers_[1], data['trainingX'][face:(face+1)]).show()

    plot_conv_weights(network.layers_[1], figsize=(3, 3))

if __name__ == '__main__':
    main()
