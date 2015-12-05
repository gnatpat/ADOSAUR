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
  return data


def splitData(dataArray, sizeChunks):
  splitArray = [dataArray[i:i + sizeChunks] for i in range(0, len(dataArray), sizeChunks)]
  # remove the extra array which is not sizeChunks long
  splitArray.pop()
  finalSplitArray = np.empty(shape=(len(splitArray), 1, 2, sizeChunks))
  # add an extra row of zeros so we can do 2D convolution
  extraZeros = np.array([0] * sizeChunks)
  i = 0
  for elem in splitArray:
	  arrayToAdd = np.vstack((elem, extraZeros))
	  finalSplitArray[i] = arrayToAdd
	  i += 1
  return finalSplitArray


def createLabelDict(labelPath):
  labelDict = {}
  for file in os.listdir(labelPath):
    csvReader = csv.reader(open(labelPath + file))
    for label in csvReader:
      labelDict[file[:-4]] = int(label[0])
  return labelDict


def buildAudioData(rawAudioPath):
  trainLabelsDict = createLabelDict('../rawData/labels/Training/')
  devLabelsDict   = createLabelDict('../rawData/labels/Development/')
  testLabelsDict  = createLabelDict('../rawData/labels/Testing/')

  currDir = os.getcwd()
  rawAudioPath = currDir + '/' + rawAudioPath
  print "Building training data..."
  trainingX, trainingY       = buildExamplesAndTargets(trainLabelsDict, rawAudioPath)
  print "Building development data..."
  developmentX, developmentY = buildExamplesAndTargets(devLabelsDict, rawAudioPath)
  print "Building test data..."
  testX, testY               = buildExamplesAndTargets(testLabelsDict, rawAudioPath)

  os.chdir(currDir)
  return trainingX, trainingY, developmentX, developmentY, testX, testY

def buildExamplesAndTargets(dictionary, path):
  X = np.empty(shape=(1, 1, 2, 10000))
  Y = np.empty(shape=(1,63))

  os.chdir(path)
  i = 0
  for key, value in dictionary.iteritems():
    for file in glob.glob("*" + key + "*.wav"):
      if i > 5:
          break
      i += 1
      audioData = getAudioData(path + file)
      splitArray = splitData(audioData, 10000)
      numExamples = len(splitArray)
      yLabels = np.array([value] * numExamples)
      yLabels = np.reshape(yLabels, (-1,1))
      X = np.concatenate((X,splitArray))
      Y = np.concatenate((Y, yLabels))
  return X, Y
