import numpy as np
import theano
import theano.tensor as T
import lasagne
import cPickle
import time
from utils import LoadData as LD
from utils import AudioDataFormatter as ADF

def buildCNN(inputVar=None):

  nonlin = lasagne.nonlinearities.rectify

  network = lasagne.layers.InputLayer(shape=(None, 1, 2, 10000), input_var=inputVar)

  network = lasagne.layers.Conv2DLayer(
                      network, num_filters=20, filter_size=(2,2),
                      nonlinearity=nonlin,
                      W=lasagne.init.GlorotUniform())

  # network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2,2))

  network = lasagne.layers.DenseLayer(network, num_units=20, nonlinearity=nonlin)
  network = lasagne.layers.DenseLayer(network, num_units=63, nonlinearity=nonlin)

  return network


# Define number of epochs
numEpochs = 500

# trainingX, trainingY, developmentX, developmentY, testX, testY = LD.loadData()
trainingX, trainingY, developmentX, developmentY, testX, testY = ADF.buildAudioData('../rawData/RawAudio/wav/')

# Prepare Theano variables for inputs and targets
inputVar = T.tensor4('inputs')
targetVar = T.matrix('targets')

# Create CNN
print "Building CNN..."
network = buildCNN(inputVar)

# Create a loss expression for training
prediction = lasagne.layers.get_output(network)
loss = lasagne.objectives.squared_error(prediction, targetVar)
loss = loss.mean()

# Create update expression for training
params = lasagne.layers.get_all_params(network, trainable=True)
updates = lasagne.updates.sgd(loss, params, learning_rate=0.01)

# Create a loss expression for validation and testing
testPrediction = lasagne.layers.get_output(network, deterministic=True)
testLoss = lasagne.objectives.squared_error(testPrediction, targetVar)
testLoss = testLoss.mean()

# Create an expression for classification accuracy
testAcc = T.mean(T.eq(T.argmax(testPrediction, axis=1), targetVar),
                  dtype=theano.config.floatX)

# Compile a function performing training step and returning corresponsing training loss
trainFn = theano.function([inputVar, targetVar], loss, updates=updates, allow_input_downcast=True)
# Compile a function computing the validation loss and accuracy
valFn = theano.function([inputVar, targetVar], [testLoss, testAcc], allow_input_downcast=True)

# Launch training loop over epochs
print "Launching training "
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
	        epoch + 1, numEpochs, time.time() - startTime))
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
