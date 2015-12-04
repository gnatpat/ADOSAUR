import theano
import theano.tensor as T
import lasagne
import DataFormatter
import numpy as np
import time

def buildCNN(input_var=None):

    # Input layer
    network = lasagne.layers.InputLayer(shape=(None, 1, 10000),
                                        input_var=input_var)
    # Convolutional layer
    network = lasagne.layers.Conv1DLayer(
            network, num_filters=20, filter_size=10,
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())
    
    # Max-pooling layer
    network = lasagne.layers.MaxPool1DLayer(network, pool_size=1)

    # Another convolutional layer and max-pooling layer
    network = lasagne.layers.Conv1DLayer(
            network, num_filters=20, filter_size=10,
            nonlinearity=lasagne.nonlinearities.rectify)
    network = lasagne.layers.MaxPool1DLayer(network, pool_size=1)

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

# Define number of epochs
numEpochs = 500
# Get data and targets from our DataFormatter
trainingX, trainingY, developmentY, developmentY, testX, testY = DataFormatter.buildAudioData("../raw_data/RawAudio/wav/")

# Prepare Theano variables for inputs and targets
inputVar = T.tensor3('inputs')
targetVar = T.ivector('targets')

# Create CNN
network = buildCNN(inputVar)

# Create a loss expression for training
prediction = lasagne.layers.get_output(network)
loss = lasagne.objectives.categorical_crossentropy(prediction, targetVar)
loss = loss.mean()

# Create update expression for training
params = lasagne.layers.get_all_params(network, trainable=True)
updates = lasagne.updates.nesterov_momentum(
        loss, params, learning_rate=0.01, momentum=0.9)

# Create a loss expression for validation and testing
testPrediction = lasagne.layers.get_output(network, deterministic=True)
testLoss = lasagne.objectives.categorical_crossentropy(testPrediction,
                                                        targetVar)
testLoss = testLoss.mean()

# Create an expression for classification accuracy 
testAcc = T.mean(T.eq(T.argmax(testPrediction, axis=1), targetVar),
                  dtype=theano.config.floatX)

# Compile a function performing training step and returning corresponsing training loss
trainFn = theano.function([inputVar, targetVar], loss, updates=updates)
# Compile a function computing the validation loss and accuracy
valFn = theano.function([inputVar, targetVar], [testLoss, testAcc])

# Launch training loop over epochs
for epoch in range(numEpochs):
	# Do a full pass over training data
	trainErr = 0
	startTime = time.time()
	trainErr += trainFn(trainingX, trainingY)

	# Do a full pass over validation data
	devErr = 0
	devAcc = 0
	err, acc = valFn(developmentX, developmentY)
	devErr += err
	devAcc += acc

	# Print the result for this epoch
	print("Epoch {} of {} took {:.3f}s".format(
	        epoch + 1, numEpochs, time.time() - start_time))
	print("  training loss:\t\t{:.6f}".format(trainErr))
	print("  validation loss:\t\t{:.6f}".format(devErr))
	print("  validation accuracy:\t\t{:.2f} %".format(devAcc))

# After training, compute and print test error
testErr = 0
testAcc = 0
err, acc = valFn(testX, testY)
testErr += err
testAcc += acc
print("Final results:")
print("  test loss:\t\t\t{:.6f}".format(testErr))
print("  test accuracy:\t\t{:.2f} %".format(testAcc))
