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

def crossValidationOnListOfANNs(trainingData, trainingLabels, minHiddenNodes=100, maxHiddenNodes=700, stepSize=100, folds=10):
	listANNs = generateListOfANNs(minHiddenNodes, maxHiddenNodes, stepSize)
	errors = []

	fileID = open('crossValidationResults.txt', 'w')
	fileID.write('crossValidationResults\n\n')

	for ann in listANNs:
		avgError = crossValidation(trainingData, trainingLabels, ann)

		# Write to output file
		fileID.write('##############################\n')
		fileID.write('# Hidden:\t{0}\n'.format(ann.num_hidden))
		fileID.write('# Cycles:\t{0}\n'.format(ann.cycles))
		fileID.write('# avgError:\t{0}\n'.format(avgError))
		fileID.write('##############################\n\n')

		errors.append(("numHiddenNodes = {0}".format(ann.num_hidden), "avgError = {0}".format(avgError)))

	return errors


def crossValidation(trainingData, trainingLabels, ann, folds=10):

	trainingDataSets, trainingLabelSets = getFolds(trainingData, trainingLabels)
	errors = []  # contains all 10 errors for each fold

	for foldIndex in range(folds):

		print "#############", foldIndex, "#############"

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

def compareActualOutputWithExpectedOutput(ann, example):
    input = np.array(trainingData[example])
    expected_output = np.array(trainingLabels[example])
    output, error = ann.run(input, expected_output)
    output = np.around(output, decimals=3)

    print "ERROR =", error

    x_values = range(DataBuilder.NUM_LABELS)
    y_values = output
    plt.plot(x_values,y_values)
    x = list(trainingLabels[example]).index(1)
    y = 0.2
    plt.xlim([-1,4])
    plt.plot((x, x), (0, y), 'r-')
    plt.show()



trainingData, trainingLabels = DataBuilder.buildANNdata()
ann = ANN(1000, num_outputs=DataBuilder.NUM_LABELS)
ann.learn_from(trainingData, trainingLabels)
compareActualOutputWithExpectedOutput(ann, 40)

# crossValidationOnListOfANNs(trainingData, trainingLabels, minHiddenNodes=10, maxHiddenNodes=100, stepSize=10)

# print crossValidation(trainingData, trainingLabels, ann)
