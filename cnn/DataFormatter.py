import scipy.io.wavfile
import os
import csv
import glob
import cPickle
import numpy as np

def getAudioData(audioPath):
	data = scipy.io.wavfile.read(audioPath)[1]
	if len(data.shape) == 2:
		return data[:, 0]
	else:
		return data


def splitData(dataArray, sizeChunks):
    splittedArray = [dataArray[i:i + sizeChunks] for i in range(0, len(dataArray), sizeChunks)]
    splittedArray.pop()
    return np.array(splittedArray)


def createLabelDict(labelPath):
	labelDict = {}
	for file in os.listdir(labelPath):
		csvReader = csv.reader(open(labelPath + file))
		for label in csvReader:
			labelDict[file[:-4]] = int(label[0])
	return labelDict


def buildAudioData(rawAudioPath):
	trainLabelsDict = createLabelDict('../database/labels/Training/')
	devLabelsDict = createLabelDict('../database/labels/Development/')
	testLabelsDict = createLabelDict('../database/labels/Testing/')

	currDir = os.getcwd()
	# change this path to wherever your raw audio wav files are
	rawAudioPath = currDir + '/' + rawAudioPath
	trainingX, trainingY       = buildExamplesAndTargets(trainLabelsDict, rawAudioPath)
	developmentX, developmentY = buildExamplesAndTargets(devLabelsDict, rawAudioPath)
	testX, testY               = buildExamplesAndTargets(testLabelsDict, rawAudioPath)

	os.chdir(currDir)
	return trainingX, trainingY, developmentX, developmentY, testX, testY

def buildExamplesAndTargets(dictionary, path):
	X = np.empty(shape=(1, 1, 10000))
	Y = np.empty(shape=(1))

	os.chdir(path)

	for key, value in dictionary.iteritems():
		for file in glob.glob("*" + key + "*.wav"):
			audioData = getAudioData(path + file)
			splittedArray = splitData(audioData, 10000)
			numExamples = len(splittedArray)
			yLabels = [value] * numExamples
			print file
			X = np.concatenate((X,splittedArray.reshape(numExamples, 1, 10000)))
			Y = np.concatenate((Y, yLabels))
	return X, Y

# trainingX, trainingY, developmentX, developmentY, testX, testY = buildAudioData('../rawData/RawAudio/wav/')
#
#
# os.chdir('../pickledData/')

# print "Pickling training..."
# f = file('trainingX.save', 'wb')
# cPickle.dump(trainingX, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()
# f = file('trainingY.save', 'wb')
# cPickle.dump(trainingY, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()

# print "Pickling development..."
# f = file('developmentX.save', 'wb')
# cPickle.dump(developmentX, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()
# f = file('developmentY.save', 'wb')
# cPickle.dump(developmentY, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()
#
# print "Pickling test..."
# f = file('testX.save', 'wb')
# cPickle.dump(testX, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()
# f = file('testY.save', 'wb')
# cPickle.dump(testY, f, protocol=cPickle.HIGHEST_PROTOCOL)
# f.close()
