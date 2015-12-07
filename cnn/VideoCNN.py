from __future__ import print_function

import numpy as np

import theano
import theano.tensor as T

import lasagne

def loadData():
    return None

def buildCNN(width, height, input_var):

    # Start by creating an input layer for the CNN
    network = lasagne.layers.InputLayer(shape=(None, 3, width, height), input_var=input_var)

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

    # Fully connected layer of 256 units with 50% dropout
    netowrk = lasagne.layers.DenseLayer(
          lasagne.layers.dropout(network, p=0.5),
          num_units=10,
          nonlinearity=lasagne.nonlinearities.softmax)

    return network

# ############################# Batch iterator ###############################
# This is just a simple helper function iterating over training data in
# mini-batches of a particular size, optionally in random order. It assumes
# data is available as numpy arrays. For big datasets, you could load numpy
# arrays as memory-mapped files (np.load(..., mmap_mode='r')), or write your
# own custom data iteration function. For small datasets, you can also copy
# them to GPU at once for slightly improved performance. This would involve
# several changes in the main program, though, and is not demonstrated here.

def iterateMinibatches(inputs, targets, batchsize):
    assert len(inputs) == len(targets)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


# Load the data
xTrain, yTrain, xVal, yVal, xTest, yTest = loadData()

inputVar = T.tensor4('inputs')
targetVar = T.ivector('targets')

network = buildCNN(640, 480, inputVar)

# Create loss expression for training
prediction = lasagne.layers.get_output(network)
loss = lasagne.objectives.categorical_crossentropy(prediction, targetVar)
loss = loss.mean()

# Use Stochastic Gradient Descent with Nesterov Momentum for training
params = lasagne.layers.get_all_params(network, trainable=True)
updates = lasagne.updates.nesterov_momentum(loss, params, learning_rate=0.01, momentum=0.9)

# Create a loss expression for validation/testing. The crucial difference
# here is that we do a deterministic forward pass through the network,
# disabling dropout layers.
testPrediction = lasagne.layers.get_output(network, deterministic=True)
testLoss = lasagne.objectives.categorical_crossentropy(testPrediction, targetVar)
testLoss = testLoss.mean()

# As a bonus, also create an expression for the classification accuracy:
testAcc = T.mean(T.eq(T.argmax(testPrediction, axis=1), targetVar),
                  dtype=theano.config.floatX)

# Compile a function performing a training step on a mini-batch (by giving
# the updates dictionary) and returning the corresponding training loss:
trainFn = theano.function([inputVar, targetVar], loss, updates=updates)

# Compile a second function computing the validation loss and accuracy:
valFn = theano.function([inputVar, targetVar], [testLoss, testAcc])

# Finally, launch the training loop.
numEpochs = 10
print("Start training.........")
for epoch in range(numEpochs):
    # Train!
    trainErr = 0
    trainBatches = 0

    for batch in iterateMinibatches(xTrain, yTrain, 100):
        inputs, targets = batch
        trainErr += trainFn(inputs, targets)
        trainBatches += 1

    # Validate!
    valErr = 0
    valAcc = 0
    valBatches = 0
    
    for batch in iterateMinibatches(xVal, yVal, 100):
        inputs, targets = batch
        err, acc = valFn(inputs, targets)
        valErr += err
        valAcc += acc
        valBatches += 1


    # Print results
    print("Finished epoch {} of {}".format(epoch+1, numEpochs))
    print("    training loss:\t\t{:.6f}".format(trainErr/trainBatches))
    print("    validation loss:\t\t{:.6f}".format(valErr/valBatches))
    print("    validation accuracy:\t\t{:.6f}".format(valAcc/valBatches))


# Test!
testErr = 0
testAcc = 0
testBatches = 0

for batch in iterateMinibatches(xTest, yTest, 100):
    inputs, targets = batch
    err, acc = valFn(inputs, targets)
    testErr += err
    testAcc += acc
    testBatches += 1

print("FINAL RESULTS")
print("   test loss:\t\t\t{:.6f}".format(testErr/testBatches))
print("   test accuracy:\t\t\t{:.2f} %".format(testAcc/testBatches * 100))

