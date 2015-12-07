import lasagne

def build_cnn(width, height):

    # Start by creating an input layer for the CNN
    network = lasagne.layers.InputLayer(shape=(None, 3, width, height))

    # Add a convolutional layer, 32 kernels of size 7x7
    network = lasagne.layers.Conv2DLayer(
          network, num_filters=32, filter_size=(7,7),
          nonlinearity=lasagne.nonlinearities.rectify,
          W=lasagne.init.GlorotUniform())

    # Max-pooling layers of factor 2 in both dimensions
    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(4, 4))

    # Add a convolutional layer, 32 kernels of size 7x7
    network = lasagne.layers.Conv2DLayer(
          network, num_filters=32, filter_size=(7,7),
          nonlinearity=lasagne.nonlinearities.rectify,
          W=lasagne.init.GlorotUniform())

    # Max-pooling layers of factor 2 in both dimensions
    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(4, 4))

    # Fully connected later of 256 units with 50% dropout
    netowrk = lasagne.layers.DenseLayer(
          lasagne.layers.dropout(network, p=0.5),
          num_units=10,
          nonlinearity=lasagne.nonlinearities.softmax)

    return network

build_cnn()
