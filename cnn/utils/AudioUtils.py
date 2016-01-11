import scipy.io.wavfile
import os
import glob
import numpy as np
import random
from Utils import createLabelDict
from collections import Counter

SIZE_CHUNKS = 96000
RAW_DATA_PATH = '../rawData/'
RAW_AUDIO_PATH = '../rawData/RawAudio/wav/mono/16k/'

def extractAudioData(audioPath):
  data = scipy.io.wavfile.read(audioPath)[1]
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


def buildAudioData(rawAudioPath=RAW_AUDIO_PATH):
  # create label dictionaries for training, dev and test sets
  trainLabelsDict = createLabelDict(RAW_DATA_PATH + 'labels/Training/')
  devLabelsDict   = createLabelDict(RAW_DATA_PATH + 'labels/Development/')
  testLabelsDict  = createLabelDict(RAW_DATA_PATH + 'labels/Testing/')

  currDir = os.getcwd()

  print "Building training data..."
  trainingX, trainingY       = buildExamplesAndTargets(trainLabelsDict, RAW_AUDIO_PATH)
  print "Building development data..."
  developmentX, developmentY = buildExamplesAndTargets(devLabelsDict, RAW_AUDIO_PATH)
  print "Building test data..."
  testX, testY               = buildExamplesAndTargets(testLabelsDict, RAW_AUDIO_PATH)

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


# performs data augmentation
def augmentData(trainingX, trainingY, developmentX, developmentY):
  trainingCount = Counter(trainingY)
  developmentCount = Counter(developmentY)

  # number of examples desired for each class
  required = 400

  print "Augmenting training data..."
  for label, count in trainingCount.iteritems():
    print "Class ", label, " augmenting..."
    extraNeeded = required - count
    # augment the data if extra examples are needed
    if extraNeeded > 0:
      for i in xrange(extraNeeded):
        # pick a random example and duplicate it
        randomExample = np.array(random.choice(trainingX)).reshape(1,1,SIZE_CHUNKS)
        trainingX = np.append(trainingX, randomExample, axis=0)
        trainingY = np.append(trainingY, np.array(label))

  print "Augmenting development data..."
  for label, count in developmentCount.iteritems():
    print "Class ", label, " augmenting..."
    extraNeeded = required - count
    # augment the data if extra examples are needed
    if extraNeeded > 0:
      for i in xrange(extraNeeded):
        # pick a random example and duplicate it
        randomExample = np.array(random.choice(developmentX)).reshape(1,1,SIZE_CHUNKS)
        developmentX = np.append(developmentX, randomExample, axis=0)
        developmentY = np.append(developmentY, np.array(label))

  return trainingX, trainingY, developmentX, developmentY
