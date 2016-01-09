import scipy.io.wavfile
import os
import glob
import numpy as np
import random
from Utils import createLabelDict
from collections import Counter

SIZE_CHUNKS = 96000

def extractAudioData(audioPath):
  data = scipy.io.wavfile.read(audioPath)[1]
  # if two channels are used, take data from the first one
  if len(data.shape) == 2:
    data = data[:, 0]
  return np.array(data, dtype='float32')


def splitData(dataArray):
  splitArray = [dataArray[i:i + SIZE_CHUNKS] for i in range(0, len(dataArray), SIZE_CHUNKS)]
  # remove the extra array which is not SIZE_CHUNKS long
  splitArray.pop()
  finalSplitArray = np.empty(shape=(len(splitArray), 1, SIZE_CHUNKS), dtype='float32')
  i = 0
  for elem in splitArray:
    # do not include the arrays with too many zeros (corresponding to silence)
    if np.count_nonzero(elem) > SIZE_CHUNKS/2:
        finalSplitArray[i] = elem
    i += 1
  return finalSplitArray


def buildAudioData(rawAudioPath):
  # create label dictionaries for training, dev and test sets
  trainLabelsDict = createLabelDict('/media/sc8013/ROXY FAT32/groupProject/rawData/labels/Training/')
  devLabelsDict   = createLabelDict('/media/sc8013/ROXY FAT32/groupProject/rawData/labels/Development/')
  testLabelsDict  = createLabelDict('/media/sc8013/ROXY FAT32/groupProject/rawData/labels/Testing/')

  currDir = os.getcwd()
  # rawAudioPath = currDir + '/' + rawAudioPath
  rawAudioPath = '/media/sc8013/ROXY FAT32/groupProject/rawData/RawAudio/wav/'
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
  X = np.empty(shape=(1,1,SIZE_CHUNKS), dtype='float32')
  Y = np.empty(shape=(0), dtype='int32')

  os.chdir(path)
  # iterate through the given dictionary
  for key, value in dictionary.iteritems():
    # iterate through the files corresponding to the patient (key)
    for file in glob.glob("*" + key + "*.wav"):
      print "Extracting data for " + file
      # extract the audio data for the current file
      audioData = extractAudioData(path + file)
      # split the audio data into arrays of size 40000
      splitArray = splitData(audioData)
      numExamples = len(splitArray)
      # create the corresponding labels to add
      yLabels = np.zeros((numExamples), dtype='int32')
      for j in range(numExamples):
          yLabels[j] = value
      # insert the data and labels to X and Y arrays
      X = np.concatenate((X,splitArray))
      Y = np.concatenate((Y, yLabels))
  # remove first element of X as this one is added when X is initialised
  # and is thus indesirable
  X = X[1:]
  return X, Y


def balanceClasses(trainingX, trainingY, developmentX, developmentY):
    trainingIndices0 = np.where(trainingY == 0)[0][:220]
    trainingIndices1 = np.where(trainingY == 1)[0][:220]
    trainingIndices2 = np.where(trainingY == 2)[0][:220]
    trainingIndices3 = np.where(trainingY == 3)[0][:220]
    
    trainingX_0 = trainingX.take(trainingIndices0, axis=0)
    trainingY_0 = np.take(trainingY, trainingIndices0)
    trainingX_1 = trainingX.take(trainingIndices1, axis=0)
    trainingY_1 = np.take(trainingY, trainingIndices1)
    trainingX_2 = trainingX.take(trainingIndices2, axis=0)
    trainingY_2 = np.take(trainingY, trainingIndices2)
    trainingX_3 = trainingX.take(trainingIndices3, axis=0)
    trainingY_3 = np.take(trainingY, trainingIndices3)

    trainingX_equal = np.append(trainingX_0, trainingX_1, axis=0)
    trainingX_equal = np.append(trainingX_equal, trainingX_2, axis=0)
    trainingX_equal = np.append(trainingX_equal, trainingX_3, axis=0)

    trainingY_equal = np.append(trainingY_0, trainingY_1, axis=0)
    trainingY_equal = np.append(trainingY_equal, trainingY_2, axis=0)
    trainingY_equal = np.append(trainingY_equal, trainingY_3, axis=0)

    developmentIndices0 = np.where(developmentY == 0)[0][:220]
    developmentIndices1 = np.where(developmentY == 1)[0][:220]
    developmentIndices2 = np.where(developmentY == 2)[0][:220]
    developmentIndices3 = np.where(developmentY == 3)[0][:220]

    developmentX_0 = developmentX.take(developmentIndices0, axis=0)
    developmentY_0 = np.take(developmentY, developmentIndices0)
    developmentX_1 = developmentX.take(developmentIndices1, axis=0)
    developmentY_1 = np.take(developmentY, developmentIndices1)
    developmentX_2 = developmentX.take(developmentIndices2, axis=0)
    developmentY_2 = np.take(developmentY, developmentIndices2)
    developmentX_3 = developmentX.take(developmentIndices3, axis=0)
    developmentY_3 = np.take(developmentY, developmentIndices3)

    developmentX_equal = np.append(developmentX_0, developmentX_1, axis=0)
    developmentX_equal = np.append(developmentX_equal, developmentX_2, axis=0)
    developmentX_equal = np.append(developmentX_equal, developmentX_3, axis=0)
    
    developmentY_equal = np.append(developmentY_0, developmentY_1, axis=0)
    developmentY_equal = np.append(developmentY_equal, developmentY_2, axis=0)
    developmentY_equal = np.append(developmentY_equal, developmentY_3, axis=0)

    return trainingX_equal, trainingY_equal, developmentX_equal, developmentY_equal


def augmentData(trainingX, trainingY, developmentX, developmentY):
  trainingCount = Counter(trainingY)
  developmentCount = Counter(developmentY)

  required = 1000
  
  print "Augmenting training data..."
  for label, count in trainingCount.iteritems():
    print "Class ", label, " augmenting..."
    extraNeeded = required - count
    if extraNeeded > 0:
      for i in xrange(extraNeeded):
        randomExample = np.array(random.choice(trainingX)).reshape(1,1,SIZE_CHUNKS)
        trainingX = np.append(trainingX, randomExample, axis=0)
        trainingY = np.append(trainingY, np.array(label))

  print "Augmenting development data..."
  for label, count in developmentCount.iteritems():
    print "Class ", label, " augmenting..."
    extraNeeded = required - count
    if extraNeeded > 0:
      for i in xrange(extraNeeded):
        randomExample = np.array(random.choice(developmentX)).reshape(1,1,SIZE_CHUNKS)
        developmentX = np.append(developmentX, randomExample, axis=0)
        developmentY = np.append(developmentY, np.array(label))

  return trainingX, trainingY, developmentX, developmentY
