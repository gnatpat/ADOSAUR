#
#  REQUIRES "test.mp4" IN CURRENT DIRECTORY
#
#  test.mp4 is currently hard coded as a 1280 x 720 video.
#  Change these parameters to match your test.mp4
#

import lasagne
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
import numpy as np
import pickle

from utils.Utils import getCNNdata


# TODO: load actual training, validation and test sets.
#       Change getCNNdata in Utils.py
def loadData():
    data = {}  # initialise dictionary
    testSet = getCNNdata('./test.mp4').reshape(-1, 1, 1280, 720)  # generate test set; -1 forces np to deduce dimension
    targets = np.array([1] * 11, dtype='int32')  # pseudo targets - NOTE: must have dtype='int32'

    # populate dictionary
    data['X_train'] = testSet  # a list of grayscale images
    data['y_train'] = targets  # a list of ints (on BDI scale)
    data['num_examples_train'] = testSet.shape[0]
    data['input_shape'] = (None,) + testSet.shape[1:]  # ignore num examples. Here input is 1280 x 720 grayscale image
    data['output_dim'] = 10  # chosen arbitrarily

    return data

def CNN(data):
    # small net for proof of concept
    # see http://goo.gl/GZUQOb for more realistic config
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
    output_num_units=data['output_dim'],
    output_nonlinearity=lasagne.nonlinearities.softmax,

    update_learning_rate=0.01,
    update_momentum=0.9,

    regression=False,
    max_epochs=3,
    verbose=1,
    )

    # Train the network
    net2.fit(data['X_train'], data['y_train'])


    # TODO: pickle trained network (after we've optimised)


    # Try the network on the first training example  -- meaningless, but whatevs
    print("\nActual:\t\t%s" % str(data['y_train'][0]))
    print("Predicted:\t%s" % str(net2.predict([data['X_train'][0]])[0]))


def main():
    data = loadData()
    print("Got %i testing datasets.\n" % len(data['X_train']))
    CNN(data)

if __name__ == '__main__':
    main()
