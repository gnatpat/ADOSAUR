import scipy.io.wavfile
import os
import csv
import glob
import cPickle

def getAudioData(audioPath):
	return scipy.io.wavfile.read(audioPath)[1]


def splitData(dataArray, sizeChunks):
    splittedArray = [dataArray[i:i + sizeChunks] for i in range(0, len(dataArray), sizeChunks)]
    splittedArray.pop()
    return splittedArray


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
	os.chdir(rawAudioPath)

	trainingX, trainingY       = buildExamplesAndTargets(trainLabelsDict, rawAudioPath)
	developmentX, developmentY = buildExamplesAndTargets(devLabelsDict, rawAudioPath)
	testX, testY               = buildExamplesAndTargets(testLabelsDict, rawAudioPath)

	return trainingX, trainingY, developmentY, developmentY, testX, testY

def buildExamplesAndTargets(dictionary, path):
	X = []
	Y = []
	os.chdir(path)

	for key, value in dictionary.iteritems():
		for file in glob.glob("*" + key + "*.wav"):
			audioData = getAudioData(path + file)
			splittedArray = splitData(audioData, 10000)
			numExamples = len(splittedArray)
			yLabels = [value] * numExamples
			X.extend(splittedArray)
			Y.extend(yLabels)

	return X, Y



buildAudioData("/media/sc8013/WD SACHA/CLEAN_AVEC/RawAudio/wav/")
