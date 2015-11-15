from ANN import ANN
import numpy as np
import DataBuilder
import matplotlib.pyplot as plt
import copy


def runDepressionANN():
	output_file = open('output','w')
	output_file.write('DepressionANN OUTPUT\n\n')

	# initialise ANN parameters
	trainingData, trainingLabels = DataBuilder.buildANNdata()

	# initialise ANN
	numInputs = len(trainingData[0])
	numHidden = 50  # whatevs
	numOutputs = DataBuilder.NUM_LABELS
	ann = ANN(numInputs, numHidden, numOutputs, cycles=10)

	# learn from data
	output, _ = ann.learn_from(trainingData, trainingLabels)

	# write output to file
	output_file.write("Running example:\n" + str(output) + "\n\n")


def getFolds(trainingData, trainingLabels, folds=10):
	trainingDataSets = []
	trainingLabelSets = []
	for i in range(0, len(trainingData), folds):
		trainingDataSets.append(trainingData[i:i+folds])
		trainingLabelSets.append(trainingLabels[i:i+folds])
	return trainingDataSets, trainingLabelSets

def generateListOfANNs(minHiddenNodes, maxHiddenNodes, stepSize):
	listANNs = []
	for numHiddenNodes in range(minHiddenNodes, maxHiddenNodes, stepSize):
		listANNs.append(ANN(numHiddenNodes))
	return listANNs

def crossValidationOnListOfANNs(trainingData, trainingLabels, minHiddenNodes=50, maxHiddenNodes=100, stepSize=10, folds=10):
	listANNs = generateListOfANNs(minHiddenNodes, maxHiddenNodes, stepSize)
	errors = []
	for ann in listANNs:
		avgError = crossValidation(trainingData, trainingLabels, ann)
		numHiddenNodes = ann.num_hidden
		print '##############################'
		print '# Hidden:\t', numHiddenNodes
		print '# Cycles:\t', ann.cycles
		print '# avgError:\t', avgError
		print '##############################'
		errors.append((numHiddenNodes, avgError))

	return errors


def crossValidation(trainingData, trainingLabels, ann, folds=10):

	trainingDataSets, trainingLabelSets = getFolds(trainingData, trainingLabels)
	errors = []  # contains all 10 errors for each fold

	for foldIndex in range(folds):

		# print "#############", foldIndex, "#############"

		# validation data and label set (10 samples)
		foldValidationDataSet = trainingDataSets[foldIndex]
		foldValidationLabelSet = trainingLabelSets[foldIndex]

		# training data and label set (90 samples)
		foldTrainingDataSets = copy.copy(trainingDataSets)
		foldTrainingLabelSets = copy.copy(trainingLabelSets)
		# remove validation set and labels
		del foldTrainingDataSets[foldIndex]
		del foldTrainingLabelSets[foldIndex]

		ann.learn_from(foldTrainingDataSets[0], foldTrainingLabelSets[0])
		for data, label in zip(foldValidationDataSet[0], foldValidationLabelSet[0]):
			_, error = ann.run(data, label)
			errors.append(error)

	return sum(errors) / len(errors)  # average error over 10 folds

def compareActualOutputWithExpectedOutput(example):
    output = np.around(ann.run(np.array(trainingData[example])), decimals=3)
    x_values = range(46)
    y_values = output
    plt.plot(x_values,y_values)
    x = list(trainingLabels[example]).index(1)
    y = 0.2
    plt.plot((x, x), (0, y), 'k-')
    plt.show()







trainingData, trainingLabels = DataBuilder.buildANNdata()
ann = ANN(50)
crossValidationOnListOfANNs(trainingData, trainingLabels, minHiddenNodes=100, maxHiddenNodes=200)
