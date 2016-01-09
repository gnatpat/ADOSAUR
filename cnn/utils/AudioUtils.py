import scipy.io.wavfile
import os
import glob
import numpy as np
import pickle
from Utils import createLabelDict
import librosa
from matplotlib.pyplot import specgram
import matplotlib.pyplot as plt

SIZE_CHUNKS = 306500
RAW_DATA_PATH = '/media/sc8013/ROXY FAT32/groupProject/rawData/'
RAW_AUDIO_PATH = '/media/sc8013/ROXY FAT32/groupProject/rawData/'

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


def buildAudioData(rawAudioPath):
  # create label dictionaries for training, dev and test sets
  trainLabelsDict = createLabelDict(RAW_DATA_PATH + 'labels/Training/')
  devLabelsDict   = createLabelDict(RAW_DATA_PATH + 'labels/Development/')
  testLabelsDict  = createLabelDict(RAW_DATA_PATH + 'labels/Testing/')

  currDir = os.getcwd()
  rawAudioPath = '/media/sc8013/ROXY FAT32/groupProject/rawData/rawAudio/wav/'
  # rawAudioPath = currDir + '/' + rawAudioPath
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
  X = np.empty(shape=(1,128,599), dtype='float32')
  Y = np.empty(shape=(0), dtype='int32')

  os.chdir(path)
  # iterate through the given dictionary
  for key, value in dictionary.iteritems():

    # iterate through the files corresponding to the patient (key)
    for file in glob.glob("*" + key + "*.wav"):

      print "Extracting data for " + file
      # extract the audio data and sampling rate for the current file
      sr, audioData = extractAudioData(path + file)
      # split the audio data into arrays of size SIZE_CHUNKS
      splitArray = splitData(audioData)
      numExamples = len(splitArray)

      # initialize the array which will contain the mel spectrograms for the file
      melSpectArray = np.empty(shape=(1,128,599), dtype='float32')

      for i in xrange(numExamples):
        # get mel spectrogram for this chunk
        melSpect = librosa.feature.melspectrogram(y=splitArray[i].reshape(-1), sr=sr)
        melSpect = np.expand_dims(melSpect, axis=0)
        melSpect = melSpect.astype(dtype='float32')
        # add it to the array
        melSpectArray = np.concatenate((melSpectArray, melSpect))
      # get rid of first useless element
      melSpectArray = melSpectArray[1:]

      # create the corresponding labels to add
      yLabels = np.zeros((numExamples), dtype='int32')
      for j in range(numExamples):
          yLabels[j] = value

      # insert the data and labels to X and Y arrays
      X = np.concatenate((X,melSpectArray))
      Y = np.concatenate((Y, yLabels))

  # remove first element of X as this one is added when X is initialised
  # and is thus indesirable
  X = X[1:]
  return X, Y

def main():
  sr, data = extractAudioData(RAW_DATA_PATH + RAW_AUDIO_PATH + 'Northwind__230_1_Northwind_audio_mono_16k.wav')
  plt.specgram(data, NFFT=2048)
  plt.show()
  
if __name__ == '__main__':
    main()
