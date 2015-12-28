import cv2
import os
import csv
import glob
import math
import numpy as np
import cPickle
import shutil
import pickle  # internet too slow to install cPickle - someone fix this!


# TODO: load actual training, validation and test sets.
#
#       Need a function taking the directory 'database'
#       which returns X_train, y_train; a numpy array of
#       grayscale images and their corresponding BDI.
#       From here, NoLearn will split these datasets into
#       training, validation and test sets.
#
def getCNNdata(filepath):
    if os.path.exists('./CNNtestSet.save'):  # check if it exists first
        return pickle.load(open('./CNNtestSet.save', 'r'))
    else:
        CNNtestSet = extractImagesfromVideo(filepath)
        pickle.dump(CNNtestSet, open('CNNtestSet.save', 'w'))
        return CNNtestSet


# filepath './test.mp4'
# Output is an array of images (RGB or grayscale)
def extractImagesfromVideo(filepath, grayscale=True):
    tempDir = '../tmp/'
    fileExt = '.jpg'

    # extract frames into temp directory
    extractFramesFromVideo(filepath, tempDir)

    # return a list of all files in temp directory e.g. ['1.jpg', ... , '5.jpg']
    filenames = glob.glob(tempDir + '*' + fileExt)  # '../temp/*.jpg'

    images = []  # stores the extracted images
    for filename in filenames:  # convert each file in tmp to an image
        if grayscale:
            images.append(extractGrayScale(filename))
        else:  # RGB
            images.append(extractRGB(filename))

    # delete temp directory after all files have been processed
    if os.path.exists(tempDir):  # check if directory exists first
        shutil.rmtree(tempDir)  # delete directory

    # return a numpy array of shape (numImages, height, width, channels)
    return np.array(images)


# Takes image and returns a 2D numpy array of tuples (R,G,B)
def extractRGB(filepath):
    return cv2.imread(filepath)


# Takes image and returns a 2D numpy array of integers [0, 255]
def extractGrayScale(filepath):
    return cv2.imread(filepath, 0)


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
