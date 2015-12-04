import scipy.io.wavfile
import os
import csv
import glob
import numpy as np

def getAudioData(audioPath):
	data = scipy.io.wavfile.read(audioPath)[1]
	# if two channels are used, take data from the first one
	if len(data.shape) == 2:
		data = data[:, 0]
	# add extra zeros to do 2d convolution
	# extraZeros = np.array([0] * len(data))
	# data = np.vstack((data, extraZeros))
	return data


def splitData(dataArray, sizeChunks):
  splitArray = [dataArray[i:i + sizeChunks] for i in range(0, len(dataArray), sizeChunks)]
  # remove the extra array which is not sizeChunks long
  splitArray.pop()
  return np.array(splitArray)


def createLabelDict(labelPath):
	labelDict = {}
	for file in os.listdir(labelPath):
		csvReader = csv.reader(open(labelPath + file))
		for label in csvReader:
			labelDict[file[:-4]] = int(label[0])
	return labelDict


def buildAudioData(rawAudioPath):
	trainLabelsDict = createLabelDict('../../rawData/labels/Training/')
	devLabelsDict   = createLabelDict('../../rawData/labels/Development/')
	testLabelsDict  = createLabelDict('../../rawData/labels/Testing/')

	currDir = os.getcwd()
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
			splitArray = splitData(audioData, 10000)
			numExamples = len(splitArray)
			yLabels = [value] * numExamples
			X = np.concatenate((X,splitArray.reshape(numExamples, 1, 10000)))
			Y = np.concatenate((Y, yLabels))
	return X, Y


trainingX, trainingY, developmentX, developmentY, testX, testY = buildAudioData('../../rawData/RawAudio/wav/')
