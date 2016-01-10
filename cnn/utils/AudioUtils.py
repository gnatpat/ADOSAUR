import scipy.io.wavfile
import os
import glob
import numpy as np
import pickle
from Utils import createLabelDict
from Utils import extractGrayScale

RAW_DATA_PATH = '../rawData/'
RAW_AUDIO_PATH = '../rawData/RawAudio/specgrams/all/'

def extractAudioData(audioPath):
  sr, data = scipy.io.wavfile.read(audioPath)
  # if two channels are used, take data from the first one
  if len(data.shape) == 2:
    data = data[:, 0]
  return sr, np.array(data, dtype='float32')


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

  print "Building training data..."
  trainingX, trainingY       = buildExamplesAndTargets(trainLabelsDict, rawAudioPath)
  print "Building development data..."
  developmentX, developmentY = buildExamplesAndTargets(devLabelsDict, rawAudioPath)
  print "Building test data..."
  testX, testY               = buildExamplesAndTargets(testLabelsDict, rawAudioPath)

  return trainingX, trainingY, developmentX, developmentY, testX, testY

def buildExamplesAndTargets(dictionary, path):
  # initialise the arrays to store inputs (X) and corresponding labels (Y)
  X = np.empty(shape=(1,256,768), dtype='float32')
  Y = np.empty(shape=(0), dtype='int32')

  currDir = os.getcwd()
  os.chdir(path)

  # iterate through the given dictionary
  for key, value in dictionary.iteritems():

    # iterate through the files corresponding to the patient (key)
    for file in glob.glob("*" + key + "*.jpg"):

      print "Extracting data for " + file
      imageData = extractGrayScale(file)
      # ignore shorter spectrograms
      if imageData.shape == (256,768):
          imageData = np.reshape(imageData, (1,256,768))
          label = np.array([value])
          X = np.concatenate((X,imageData))
          Y = np.concatenate((Y, label))

  # remove first element of X as this one is added when X is initialised
  # and is thus indesirable
  X = X[1:]

  os.chdir(currDir)

  return X, Y
