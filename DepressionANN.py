from ANN import ANN
import numpy as np
import DataBuilder

# initialise ANN parameters
trainingData, trainingLabels = DataBuilder.buildANNdata()

# initialise ANN
num_inputs = len(trainingData[0])
num_hidden = 1000  # whatevs
num_outputs = DataBuilder.NUM_LABELS
ann = ANN(num_inputs, num_hidden, num_outputs, cycles=1000)

# learn from data
ann.learn_from(trainingData, trainingLabels)

EXAMPLE = 3
print "Running first example:\n", np.around(ann.run(np.array(trainingData[EXAMPLE])), decimals=3)
print "Expected label:\n", trainingLabels[EXAMPLE]
