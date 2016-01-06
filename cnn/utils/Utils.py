import csv
import os
from sklearn.metrics import classification_report, accuracy_score

# E.g. createLabelDict('../rawData/labels/Training/')
# Takes path to data file and outputs dictionary with key
# as patient and label as score on BDI scale
def createLabelDict(labelPath):
    labelDict = {}
    for file in os.listdir(labelPath):
        csvReader = csv.reader(open(labelPath + file))
        for label in csvReader:
            labelNo = int(int(label[0])/16)
            labelDict[file[:-4]] = labelNo
    return labelDict

# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    print("\nTesting network...")
    predictions = network.predict(inputs)
    print(classification_report(expectedLabels, predictions))
    print("The accuracy is: ", accuracy_score(expectedLabels, predictions))

# Saves network
def saveNet(filename=None, network=None):
    f = open(filename, 'wb')
    cPickle.dump(network, f, -1)
    return None

# Loads network
def loadNet(filename=None):
    f = open(filename, 'rb')
    net = cPickle.load(f)
    return net
