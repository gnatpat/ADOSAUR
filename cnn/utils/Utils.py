import csv
import os
import cPickle
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from collections import Counter

# E.g. createLabelDict('../rawData/labels/Training/')
# Takes path to data file and outputs dictionary with key
# as patient and label as score on BDI scale
def createLabelDict(labelPath):
    labelDict = {}
    for file in os.listdir(labelPath):
        csvReader = csv.reader(open(labelPath + file))
        for label in csvReader:
            labelToAdd = int(label[0])
            # 0-9 minimal depression
            if labelToAdd in range(0,10):
                labelToAdd = 0
            # 10-18 = mild depression
            elif labelToAdd in range(10,19):
                labelToAdd = 1
            # 19-29 = moderate depression
            elif labelToAdd in range(19,30):
                labelToAdd = 2
            # 30-63 = severe depression
            elif labelToAdd in range(30,64):
                labelToAdd = 3
            labelDict[file[:-4]] = labelToAdd
    return labelDict

# Tests a network using test data and expected labels,
# printing the classification report and accuracy score
def testCNN(network, inputs, expectedLabels):
    print("\nTesting network...")
    predictions = network.predict(inputs)
    print("Predictions: ", Counter(predictions))
    print("Expected: ", Counter(expectedLabels))
    print(classification_report(expectedLabels, predictions))
    print(confusion_matrix(expectedLabels, predictions))
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
