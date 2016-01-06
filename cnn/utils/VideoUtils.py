import cv2
import os
import csv
from glob import glob
import math
import numpy as np
import shutil
import pickle

from Utils import createLabelDict

DATABASE_DIR = '../rawData/'
VIDEO_FOLDER = 'rawVideo/'
LABEL_FOLDER = 'labels/'


# filepath './test.mp4'
# Output is an array of images (RGB or grayscale)
def extractImagesfromVideo(filepath, grayscale=True):
    tempDir = '../tmp/'
    fileExt = '.jpg'

    # extract frames into temp directory
    extractFramesFromVideo(filepath, tempDir)

    # return a list of all files in temp directory e.g. ['1.jpg', ... , '5.jpg']
    filenames = glob(tempDir + '*' + fileExt)  # '../temp/*.jpg'

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
    filename = filepath.split('/')[-1][:-4]  # exclude extension
    vc = cv2.VideoCapture(filepath)  # initialise video capture

    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)

    second = 0  # current second in video
    capRate = 5  # time between captures
    numberOfFrames = vc.get(7)
    currentFrame = 0
    vc.set(0, 0);
    while currentFrame < numberOfFrames: # still receiving data
        success, image = vc.read()
        if success:
            cv2.imwrite(outputPath + filename + '_' + str(second) + '.jpg', image)
            second += capRate
        else:
            break  # couldn't read image

        vc.set(0, second * 1000)  # set capturing position to (second * 1000) ms
        currentFrame = vc.get(1)
    vc.release()  # release camera
    return None


def getCNNdata(CNNfolder='./'):

    print '\n\nLoading training data...'
    [trainingDir] \
        = glob(CNNfolder + DATABASE_DIR + VIDEO_FOLDER + 'Training')
    trainingLabelDict \
        = createLabelDict(CNNfolder + DATABASE_DIR + LABEL_FOLDER + 'Training/')
    trainingX, trainingY \
        = retrieveDataFrom(trainingDir, trainingLabelDict)
    trainingX = trainingX.reshape(-1, 1, trainingX.shape[1], trainingX.shape[2])

    print '\n\nLoading validation data...'
    [validationDir] \
        = glob(CNNfolder + DATABASE_DIR + VIDEO_FOLDER + 'Development')
    validationLabelDict \
        = createLabelDict(CNNfolder + DATABASE_DIR + LABEL_FOLDER + 'Development/')
    validationX, validationY \
        = retrieveDataFrom(validationDir, validationLabelDict)
    validationX = validationX.reshape(-1, 1, validationX.shape[1], validationX.shape[2])

    print '\n\nLoading testing data...'
    [testingDir] \
        = glob(CNNfolder + DATABASE_DIR + VIDEO_FOLDER + 'Testing')
    testingLabelDict \
        = createLabelDict(CNNfolder + DATABASE_DIR + LABEL_FOLDER + 'Testing/')
    testingX, testingY \
        = retrieveDataFrom(testingDir, testingLabelDict)
    testingX = testingX.reshape(-1, 1, testingX.shape[1], testingX.shape[2])

    return trainingX, trainingY, validationX, validationY, testingX, testingY

# retrieve videos from subdirectories within current directory
def retrieveDataFrom(directory, labelsDict):
    rawVideoPaths = ([ glob(x + '/*') for x in glob(directory + '/[!p]*') ])
    videoPaths = []
    for folder in rawVideoPaths:
        for path in folder:
            videoPaths.append(path)
    images = []
    labels = []
    videoPaths = videoPaths[0:8]
    for videoPath in videoPaths:
        videoPath = ''.join(videoPath)
        filename = videoPath.split('/')[-1][:-4]  # e.g. 203_1_Northwind_video
        patientNum = filename[:5]  # e.g. 203_1
        # print patientNum, 'has label', labelsDict[patientNum]
        picklePath = directory + '/pickledData/' + filename + '.save'
        if os.path.exists(picklePath):  # check if it exists first
            print 'Loading pickled data of ' + filename
            curImages = pickle.load(open(picklePath, 'r'))
        else:
            print 'Extracting data for ' + filename
            curImages = extractImagesfromVideo(videoPath)
            if not os.path.exists(directory + '/pickledData/'):
                os.mkdir(directory + '/pickledData/')  # pickle dir doesn't exist so make it
            print 'Pickling data in ' + picklePath
            pickle.dump(curImages, open(picklePath, 'w'))
        images.extend(curImages)  # add images to list of examples
        labels.extend([labelsDict[patientNum]] * len(curImages))  # assign corresponding label
    return np.array(images), np.array(labels, dtype='int32')


if __name__ == '__main__':
    trainingX, trainingY, validationX, validationY, testingX, testingY \
        = getCNNdata('../')

    # print trainingX.shape
    # print trainingY.shape
    # print validationX.shape
    # print validationY.shape
    # print testingX.shape
    # print testingY.shape
