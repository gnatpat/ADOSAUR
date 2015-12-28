import scipy.io.wavfile
import os
import glob
import numpy as np
from Utils import createLabelDict

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
  finalSplitArray = np.empty(shape=(len(splitArray), 1, sizeChunks))
  i = 0
  for elem in splitArray:
   finalSplitArray[i] = elem
   i += 1
  return finalSplitArray


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
  X = np.empty(shape=(1, 1, 10000))
  Y = np.empty(shape=(1))

  os.chdir(path)
  i = 0
  for key, value in dictionary.iteritems():
    for file in glob.glob("*" + key + "*.wav"):
      if i > 10:
          break
      i += 1
      audioData = getAudioData(path + file)
      splitArray = splitData(audioData, 10000)
      numExamples = len(splitArray)
      yLabels = np.zeros((numExamples))
      for j in range(numExamples):
          yLabels[j] = value
      X = np.concatenate((X,splitArray))
      Y = np.concatenate((Y, yLabels))
  return X, Y
