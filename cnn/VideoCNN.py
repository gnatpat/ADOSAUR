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

from utils.Utils import getCNNtestSet


# TODO: load actual training, validation and test sets. See Utils.py
def loadData():
    data = {}  # initialise dictionary
    testSet = getCNNtestSet('./test.mp4').reshape(-1, 1, 1280, 720)  # generate test set; -1 forces np to deduce dimension
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
    data['output_dim'] = 10

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
    output_num_units=data['output_dim'], output_nonlinearity=lasagne.nonlinearities.softmax,

    update_learning_rate=0.01,
    update_momentum=0.9,

    regression=False,
    max_epochs=3, # was 1000
    verbose=1,
    )

    # Train the network
    net2.fit(data['X_train'], data['y_train'])

    # # Save trained network
    # pickle.dump(net2, open('CNN.save','w'))

    # Try the network on new data
    print("\nActual:\t\t%s" % str(data['y_test'][0]))
    print("Predicted:\t%s" % str(net2.predict([data['X_test'][0]])[0]))


def main():
    data = loadData()
    print("Got %i testing datasets.\n" % len(data['X_train']))
    CNN(data)

if __name__ == '__main__':
    main()
