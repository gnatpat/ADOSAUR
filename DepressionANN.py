from ANN import ANN
import numpy as np
import DataBuilder
import matplotlib.pyplot as plt

output_file = open('output','w')
output_file.write('DepressionANN OUTPUT\n\n')

# initialise ANN parameters
trainingData, trainingLabels = DataBuilder.buildANNdata()

# initialise ANN
num_inputs = len(trainingData[0])
num_hidden = 50  # whatevs
num_outputs = DataBuilder.NUM_LABELS
ann = ANN(num_inputs, num_hidden, num_outputs, cycles=10)

# learn from data
output = ann.learn_from(trainingData, trainingLabels)

# write output to file
output_file.write("Running example:\n" + str(output) + "\n\n")

def compareActualOutputWithExpectedOutput(example):
    output = np.around(ann.run(np.array(trainingData[example])), decimals=3)
    x_values = range(46)
    y_values = output
    plt.plot(x_values,y_values)
    x = list(trainingLabels[example]).index(1)
    y = 0.2
    plt.plot((x, x), (0, y), 'k-')
    plt.show()

compareActualOutputWithExpectedOutput(3)
