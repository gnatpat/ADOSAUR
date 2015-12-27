import cv2
import os
import csv
import glob
import math
import numpy as np
import cPickle


# filepath './test.mp4'
def extractRGBfromVideo(filepath):
    tempDir = '../tmp/'
    fileExt = '.jpg'

    # extract frames into temp directory
    extractFramesFromVideo(filepath, tempDir)

    # return a list of all jpegs in temp directory e.g. ['1.jpg', ... , '5.jpg']
    filenames = glob.glob(tempDir + '*' + fileExt)  # '../temp/*.jpg'

    rgbConversions = []  # stores the converted RGB files
    for filename in filenames:  # convert each file in temp to RGB
        rgbConversions.append(extractRGB(filename))

    # delete temp directory after all files have been converted to RGB
    if os.path.exists(tempDir):  # check if it exists first
        import shutil
        shutil.rmtree(tempDir)  # delete directory

    # return a numpy array of shape (frames, height, width, channels)
    return np.array(rgbConversions)


# Takes image and returns a numpy array of tuples (R,G,B)
def extractRGB(filepath):
    return cv2.imread(filepath)


# Takes video file path and outputs frames numbered 1.jpg, 2.jpg, ...
# into the output folder (e.g. outputImages/)
def extractFramesFromVideo(filepath, outputPath):
    vc = cv2.VideoCapture(filepath)  # initialise video capture
    count = 1  # frame count

    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)

    # The following extracts frames every second
    frameRate = math.floor(vc.get(5))  # get video frame rate
    while vc.isOpened(): # still receiving data
        frameNum = math.floor(vc.get(1))  # get current frame number
        rval, frame = vc.read()  # read frame

        if (rval == False):
            break  # no more frames
        if (frameNum % frameRate == 0):  # e.g. every 24 frames
            cv2.imwrite(outputPath + str(count) + '.jpg', frame)  # extract frame
            count += 1

    vc.release()  # release camera
    return None


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
