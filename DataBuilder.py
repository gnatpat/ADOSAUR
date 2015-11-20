import DataParser
import numpy as np
import pickle
import os

DATA_PATH = 'pickledData/'
NUM_LABELS = 46  # in AVEC challenge data

def saveParsedData():
    os.mkdir('pickledData')
    trainingData, trainingLabels, developmentData, developmentLabels, testingData = DataParser.parseAudioData()
    pickle.dump(trainingData,      open(DATA_PATH + 'trainingData.p',     'wb'))
    pickle.dump(trainingLabels,    open(DATA_PATH + 'trainingLabels.p',   'wb'))
    pickle.dump(developmentData,   open(DATA_PATH + 'developmentData.p',  'wb'))
    pickle.dump(developmentLabels, open(DATA_PATH + 'developmentLabels.p','wb'))
    pickle.dump(testingData,       open(DATA_PATH + 'testingData.p',      'wb'))

def convertLabelToArray(label):
    # Use BDI scale
    labelArray = np.zeros((1,4))
    # 0-9 = minimal depression
    if label in range(0,10):
        labelArray[0][0] = 1
    # 10-18 = mild depression
    elif label in range(10,19):
        labelArray[0][1] = 1
    # 19-29 = moderate depression
    elif label in range(19,30):
        labelArray[0][2] = 1
    # 30-63 = severe depression
    elif label in range(30,64):
        labelArray[0][3] = 1
    return labelArray[0]

def buildANNdata():

    # pickle data if not done already
    if not os.path.isdir('pickledData/'):
        saveParsedData()

    # load audio data
    trainingData   = pickle.load(open(DATA_PATH + 'trainingData.p',  'rb'))
    trainingLabels = pickle.load(open(DATA_PATH + 'trainingLabels.p','rb'))

    # convert training labels to vectors
    for i, label in enumerate(trainingLabels):
        trainingLabels[i] = convertLabelToArray(label)

    # convert to numpy arrays
    trainingData = np.array(trainingData)
    trainingLabels = np.array(trainingLabels)

    return trainingData, trainingLabels
