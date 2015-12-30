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
def buildCNN(params):

    network = NeuralNet(
        # specify the layers
        layers=[('input', lasagne.layers.InputLayer),
                ('conv1', lasagne.layers.Conv1DLayer),
                ('hidden', lasagne.layers.DenseLayer),
                ('output', lasagne.layers.DenseLayer),
                ],

        # layer parameters
        input_shape = (None, 1, 10000),
        conv1_num_filters = params["conv1_num_filters"],
        conv1_filter_size = params["conv1_filter_size"],
        hidden_num_units = params["hidden_num_units"],  # number of units in 'hidden' layer
        output_nonlinearity = lasagne.nonlinearities.softmax,
        output_num_units = 64,  # 64 target values for the depression indices

        # optimization method
        update = params["update"],

        regression = False, # classification problem
        max_epochs = 10,
        verbose = 0,

        # split the training data into training and validation using 50% for val
        train_split = TrainSplit(eval_size=0.5),
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
    # TODO: may need a fix, getting some warnings
    predictions = network.predict(inputs)
    print(classification_report(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))


def optimiseCNN(data):
    X = data['X']
    Y = data['Y']
    params = {}
    # initialise best accuracy and best params
    bestAccuracy = 0
    bestParams = {}

    # open the file for writing
    file = open("audioCNN_results.txt", "w")

    # perform a grid search through the parameters
    for update in {lasagne.updates.rmsprop, lasagne.updates.nesterov_momentum, lasagne.updates.adagrad}:
        for conv1_num_filters in xrange(5,55,5):
            for conv1_filter_size in xrange(2,22,2):
                for hidden_num_units in xrange(5,55,5):
                    print "Trying new network..."

                    # fill in params dictionary
                    params["update"]            = update
                    params["conv1_num_filters"] = conv1_num_filters
                    params["conv1_filter_size"] = conv1_filter_size
                    params["hidden_num_units"]  = hidden_num_units

                    # build and train the network with current params
                    network = buildCNN(params)
                    network.fit(X, Y)

                    # see how it performs
                    predictions = network.predict(data["testX"])
                    accuracyScore = accuracy_score(data["testY"], predictions)
                    correctlyClassified = proportionCorrect(predictions, data["testY"])
                    if (accuracyScore > bestAccuracy):
                        bestAccuracy = accuracyScore
                        bestParams = params

                    # write results to a file
                    file.write("Parameters used:\n")
                    file.write("\tupdate: " + str(update) + "\n")
                    file.write("\tconv1_num_filters: " + str(conv1_num_filters) + "\n")
                    file.write("\tconv1_filter_size: " + str(conv1_filter_size) + "\n")
                    file.write("\thidden_num_units: " + str(hidden_num_units) + "\n")
                    file.write("Accuracy score: " + str(accuracyScore) + "\n\n")
                    file.flush()

    # write optimal results found
    file.write("BEST PARAMETERS:\n")
    file.write("\tupdate: " + str(update) + "\n")
    file.write("\tconv1_num_filters: " + str(bestParams["conv1_num_filters"]) + "\n")
    file.write("\tconv1_filter_size: " + str(bestParams["conv1_filter_size"]) + "\n")
    file.write("\thidden_num_units: " + str(bestParams["hidden_num_units"]) + "\n")
    file.write("BEST ACCURACY SCORE: " + str(bestAccuracy))
    file.flush()

    file.close()


def main():
    # load our data
    data = loadAudioData()
    # optimise the cnn
    optimiseCNN(data)


if __name__ == '__main__':
    main()
