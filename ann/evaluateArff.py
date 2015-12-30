import DataParser
import DataBuilder
import numpy as np
import ANN

from random import randint

attributesData = np.array(DataParser.parseSingleArffDataFile('openSMILE/output.arff'))

trainingData, trainingLabels = DataBuilder.buildANNdata()
ann = ANN.ANN(50)
ann.learn_from(trainingData, trainingLabels)

output, _ = ann.run(attributesData, range(DataBuilder.NUM_LABELS))

print output
