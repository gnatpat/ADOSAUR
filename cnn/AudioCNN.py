import numpy as np
import theano
import theano.tensor as T
import lasagne
import time
from utils import AudioUtils as AU
from utils import Utils as utils
from nolearn.lasagne import NeuralNet
from nolearn.lasagne import TrainSplit
from sklearn.metrics import classification_report, accuracy_score


# Builds the network
def buildCNN():

    network = NeuralNet(
        # specify the layers
        layers=[('input', lasagne.layers.InputLayer),
                ('conv1', lasagne.layers.Conv1DLayer),
                ('pool1', lasagne.layers.MaxPool1DLayer),
                ('dropout1', layers.DropoutLayer),
                ('conv2', lasagne.layers.Conv1DLayer),
                ('pool2', lasagne.layers.MaxPool1DLayer),
                ('dropout2', layers.DropoutLayer),
                ('conv3', lasagne.layers.Conv1DLayer),
                ('pool3', lasagne.layers.MaxPool1DLayer),
                ('dropout3', layers.DropoutLayer)
                ('hidden4', lasagne.layers.DenseLayer),
                ('dropout4', layers.DropoutLayer),
                ('hidden5', lasagne.layers.DenseLayer),
                ('output', lasagne.layers.DenseLayer),
                ],

        # layer parameters
        input_shape = (None, 1, 10000),
        conv1_num_filters=32, conv1_filter_size=3, pool1_pool_size=2,
        dropout1_p=0.1,
        conv2_num_filters=64, conv2_filter_size=2, pool2_pool_size=2,
        dropout2_p=0.2,
        conv3_num_filters=128, conv3_filter_size=2, pool3_pool_size=2,
        dropout3_p=0.3,
        hidden4_num_units=500,
        dropout4_p=0.5,
        hidden5_num_units=500,
        output_num_units = 64,  # 64 target values for the depression indices
        output_nonlinearity = lasagne.nonlinearities.softmax,

        # optimization method
        update_learning_rate=0.01,
        update_momentum=0.9,

        regression = False, # classification problem
        max_epochs = 1,
        verbose = 1,

        # split the training data into training and validation using 30% for val
        train_split = TrainSplit(eval_size=0.3),
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

    # add the test data to dictionary
    data['testX'] = testX
    data['testY'] = testY

    return data


def trainCNN(data, params, save=True, load=False):
    # get our data
    X = data['X']
    Y = data['Y']

    if load:
        # load a pretrained network
        print("Loading the network...")
        network = utils.loadNet('audioCNN.pickle')
    else:
        # build network architecture
        network = buildCNN(params)
        # train the network
        network.fit(X, Y)

        if save:
            # pickle the network
            print("Saving the network...")
            utils.saveNet('audioCNN.pickle', network)

    return network


# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    # TODO: need to fix it, always gives the same accuracy...
    predictions = network.predict(inputs)
    print(classification_report(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))


def main():
    # load our data
    data = loadAudioData()
    # build the network
    print "Building the network..."
    params = {}
    network = buildCNN(params)
    # train the network
    print "Training the network..."
    network.fit(data['X'], data['Y'])
    # test the network
    print "Testing the network..."
    testCNN(network, data['testX'], data['testY'])


if __name__ == '__main__':
    main()
