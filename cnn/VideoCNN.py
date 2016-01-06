import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import PrintLayerInfo

import numpy as np
import pickle

from utils.VideoUtils import getCNNdata
from utils.Utils import testCNN

UNITS_ON_BDI = 3


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
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.MaxPool2DLayer, {'pool_size': (2, 2)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.MaxPool2DLayer, {'pool_size': (2, 2)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.MaxPool2DLayer, {'pool_size': (2, 2)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.Conv2DLayer, {'num_filters':32, 'filter_size':(3, 3)}),
            (layers.MaxPool2DLayer, {'pool_size': (2, 2)}),
            ('hidden2', layers.DenseLayer),
            ('output', layers.DenseLayer),
            ],
        input_shape=data['input_shape'],
        hidden2_num_units=50,
        output_num_units=data['output_dim'],
        output_nonlinearity=lasagne.nonlinearities.softmax,

        # learning parameters
        update_learning_rate=0.01,
        update_momentum=0.9,

        # miscellaneous
        regression=False,
        max_epochs=1,
        verbose=3,
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

    network = CNN(data)
    
    network.initialize()
    # layer_info = PrintLayerInfo()
    # layer_info(network)

    testCNN(network, data['testingX'], data['testingY'])

if __name__ == '__main__':
    main()
