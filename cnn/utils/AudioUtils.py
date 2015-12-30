import scipy.io.wavfile
import os
import glob
import numpy as np
from Utils import createLabelDict

def extractAudioData(audioPath):
  data = scipy.io.wavfile.read(audioPath)[1]
  # if two channels are used, take data from the first one
  if len(data.shape) == 2:
    data = data[:, 0]
  return data


def splitData(dataArray, sizeChunks):
  splitArray = [dataArray[i:i + sizeChunks] for i in range(0, len(dataArray), sizeChunks)]
  # remove the extra array which is not sizeChunks long
  splitArray.pop()
  finalSplitArray = np.empty(shape=(len(splitArray), 1, sizeChunks), dtype='float64')
  i = 0
  for elem in splitArray:
    # do not include the arrays with too many zeros (corresponding to silence)
    if np.count_nonzero(elem) > sizeChunks/2:
        finalSplitArray[i] = elem
    i += 1
  return finalSplitArray


def buildAudioData(rawAudioPath):
  # create label dictionaries for training, dev and test sets
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
  # initialise the arrays to store inputs (X) and corresponding labels (Y)
  X = np.empty(shape=(1, 1, 10000), dtype='float64')
  Y = np.empty(shape=(1), dtype='int32')

  os.chdir(path)
  i = 0
  # iterate through the given dictionary
  for key, value in dictionary.iteritems():
    # iterate through the files corresponding to the patient (key)
    for file in glob.glob("*" + key + "*.wav"):
      # extract the audio data for the current file
      audioData = extractAudioData(path + file)
      # split the audio data into arrays of size 10000
      splitArray = splitData(audioData, 10000)
      numExamples = len(splitArray)
      # create the corresponding labels to add
      yLabels = np.zeros((numExamples), dtype='int32')
      for j in range(numExamples):
          yLabels[j] = value
      # insert the data and labels to X and Y arrays
      X = np.concatenate((X,splitArray))
      Y = np.concatenate((Y, yLabels))
  return X, Y
