import cv2
import os

# E.g. createLabelDict('../rawData/labels/Training/')
# Takes path to data file and outputs dictionary with key
# as patient and label as score on BDI scale
def createLabelDict(labelPath):
    labelDict = {}
    for file in os.listdir(labelPath):
        csvReader = csv.reader(open(labelPath + file))
        for label in csvReader:
            labelDict[file[:-4]] = int(label[0])
    return labelDict

# pickel dat net duh
def saveNet(filename=None, network=None):
    f = open(filename, 'wb')
    cPickle.dump(network, f, -1)
    return None

# load da net 4rom fyl
def loadNet(filename=None):
    f = open(filename, 'rb')
    net = cPickle.load(f)
    return net
