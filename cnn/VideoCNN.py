import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
import numpy as np
import pickle

from utils.Utils import getANNtestSet, getCNNtestSet


# TODO: load actual training, validation and test sets. See Utils.py
def loadANNdata():
    data = {}  # initialise dictionary
    testSet = getANNtestSet('./test.mp4')  # generate test set
    targets = np.array([1] * 11, dtype='int32')  # pseudo targets

    # populate dictionary
    data['X_train'] = testSet
    data['y_train'] = targets
    data['X_valid'] = testSet
    data['y_valid'] = targets
    data['X_test'] = testSet
    data['y_test'] = targets
    data['num_examples_train'] = 11
    data['num_examples_valid'] = 11
    data['num_examples_test'] = 11
    data['input_dim'] = 1280 * 720
    data['output_dim'] = 15

    return data

# Regular neural network
def ANN(data):
    net1 = NeuralNet(
        layers=[('input', layers.InputLayer),
                ('hidden', layers.DenseLayer),
                ('output', layers.DenseLayer),
                ],
        # layer parameters:
        input_shape=(None, data['input_dim']),
        hidden_num_units=100,  # number of units in hidden layer
        output_nonlinearity=lasagne.nonlinearities.softmax,
        output_num_units=data['output_dim'],

        # optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.01,
        update_momentum=0.9,

        max_epochs=5,
        verbose=1,
        )

    # Train the network
    net1.fit(data['X_train'], data['y_train'])

    # Try the network on new data
    print("Feature vector (100-110): %s" % data['X_test'][0][100:110])
    print("Label: %s" % str(data['y_test'][0]))
    print("Predicted: %s" % str(net1.predict([data['X_test'][0]])))


# TODO: load actual training, validation and test sets. See Utils.py
def loadCNNdata():
    data = {}  # initialise dictionary
    testSet = getCNNtestSet('./test.mp4').reshape(-1, 1, 1280, 720)  # generate test set
    targets = np.array([1] * 11, dtype='int32')  # pseudo targets

    # populate dictionary
    data['X_train'] = testSet
    data['y_train'] = targets
    data['X_valid'] = testSet
    data['y_valid'] = targets
    data['X_test'] = testSet
    data['y_test'] = targets
    data['num_examples_train'] = 11
    data['num_examples_valid'] = 11
    data['num_examples_test'] = 11
    data['input_shape'] = (None, 1, 1280, 720)  # 1280 x 720 grayscale image input
    data['output_dim'] = 13

    return data

def CNN(data):
    # small net for proof of concept
    net2 = NeuralNet(
    layers=[
        ('input', layers.InputLayer),
        ('conv1', layers.Conv2DLayer),
        ('pool1', layers.MaxPool2DLayer),
        ('hidden2', layers.DenseLayer),
        ('output', layers.DenseLayer),
        ],
    input_shape=data['input_shape'],
    conv1_num_filters=5, conv1_filter_size=(3, 3), pool1_pool_size=(2, 2),
    hidden2_num_units=50,
    output_num_units=data['output_dim'], output_nonlinearity=None,

    update_learning_rate=0.01,
    update_momentum=0.9,

    regression=False,
    max_epochs=5, # was 1000
    verbose=1,
    )

    # net2 = NeuralNet(
    # layers=[
    #     ('input', layers.InputLayer),
    #     ('conv1', layers.Conv2DLayer),
    #     ('pool1', layers.MaxPool2DLayer),
    #     ('conv2', layers.Conv2DLayer),
    #     ('pool2', layers.MaxPool2DLayer),
    #     ('conv3', layers.Conv2DLayer),
    #     ('pool3', layers.MaxPool2DLayer),
    #     ('hidden4', layers.DenseLayer),
    #     ('hidden5', layers.DenseLayer),
    #     ('output', layers.DenseLayer),
    #     ],
    # input_shape=data['input_shape'],
    # conv1_num_filters=32, conv1_filter_size=(3, 3), pool1_pool_size=(2, 2),
    # conv2_num_filters=64, conv2_filter_size=(2, 2), pool2_pool_size=(2, 2),
    # conv3_num_filters=128, conv3_filter_size=(2, 2), pool3_pool_size=(2, 2),
    # hidden4_num_units=500, hidden5_num_units=500,
    # output_num_units=data['output_dim'], output_nonlinearity=None,
    #
    # update_learning_rate=0.01,
    # update_momentum=0.9,
    #
    # regression=True,
    # max_epochs=2, # was 1000
    # verbose=1,
    # )

    # Train the network
    net2.fit(data['X_train'], data['y_train'])

    # Save trained network
    pickle.dump(net2, open('CNN.save','w'))

    # Try the network on new data
    print("Feature vector (100-110): %s" % data['X_test'][0][100:110])
    print("Label: %s" % str(data['y_test'][0]))
    print("Predicted: %s" % str(net2.predict([data['X_test'][0]])))


def main():
    data = loadCNNdata()
    print("Got %i testing datasets.\n" % len(data['X_train']))
    CNN(data)

if __name__ == '__main__':
    main()
