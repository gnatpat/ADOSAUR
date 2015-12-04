import numpy as np
import theano
import theano.tensor as T
import lasagne
import DataFormatter
import cPickle

def buildCNN(inputVar=None):

  nonlin = lasagne.nonlinearities.rectify

  network = lasagne.layers.InputLayer(shape=(None, 1, 10000), input_var=inputVar)

  network = lasagne.layers.Conv1DLayer(
                      network, num_filters=20, filter_size=10, stride=1, pad=1,
                      nonlinearity=nonlin,
                      W=lasagne.init.GlorotUniform())

  network = lasagne.layers.MaxPool1DLayer(network, pool_size=2)

  network = lasagne.layers.DenseLayer(network, num_units=20, nonlinearity=nonlin)
  network = lasagne.layers.DenseLayer(network, num_units=63, nonlinearity=nonlin)

  return network


# Define number of epochs
numEpochs = 500

# Get data and targets from our DataFormatter
print "Loading training..."
f = file('../pickledData/trainingX.save', 'rb')
trainingX = cPickle.load(f)
f.close()

f = file('../pickledData/trainingY.save', 'rb')
trainingY = cPickle.load(f)
f.close()

print "Loading development..."
f = file('../pickledData/developmentX.save', 'rb')
developmentX = cPickle.load(f)
f.close()

f = file('../pickledData/developmentY.save', 'rb')
developmentY = cPickle.load(f)
f.close()

print "Loading test..."
f = file('../pickledData/testX.save', 'rb')
testX = cPickle.load(f)
f.close()

f = file('../pickledData/testY.save', 'rb')
testY = cPickle.load(f)
f.close()

# Prepare Theano variables for inputs and targets
inputVar = T.tensor3('inputs')
targetVar = T.ivector('targets')

# Create CNN
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
