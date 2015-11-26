import scipy.io.wavfile
import theano
import theano.tensor as T
import lasagne

def getAudioData(audioPath):
	return scipy.io.wavfile.read(audioPath)[1]

def buildCNN(input_var=None):

    # Input layer
    network = lasagne.layers.InputLayer(shape=(None, 1, 1, 10000),
                                        input_var=input_var)

    # Convolutional layer
    network = lasagne.layers.Conv1DLayer(
            network, num_filters=32, filter_size=5,
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())
    
    # Max-pooling layer
    network = lasagne.layers.MaxPool1DLayer(network, pool_size=2)

    # Another convolutional layer and max-pooling layer
    network = lasagne.layers.Conv1DLayer(
            network, num_filters=32, filter_size=5,
            nonlinearity=lasagne.nonlinearities.rectify)
    network = lasagne.layers.MaxPool2DLayer(network, pool_size=2)

    # A fully-connected layer of 256 units with 50% dropout on its inputs
    network = lasagne.layers.DenseLayer(
            lasagne.layers.dropout(network, p=.5),
            num_units=256,
            nonlinearity=lasagne.nonlinearities.rectify)

    # And, finally, the 63-unit output layer with 50% dropout on its inputs
    network = lasagne.layers.DenseLayer(
            lasagne.layers.dropout(network, p=.5),
            num_units=63,
            nonlinearity=lasagne.nonlinearities.softmax)

    return network


