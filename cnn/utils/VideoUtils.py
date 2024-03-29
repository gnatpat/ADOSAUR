import cv2
import os
import csv
from glob import glob
import math
import numpy as np
import shutil
import pickle
import threading
from Queue import Queue
from scipy.ndimage.interpolation import zoom
from Utils import createLabelDict
from Utils import loadNet
from Utils import DATABASE_DIR, LABEL_FOLDER
from collections import Counter

VIDEO_FOLDER = 'RawVideo/'

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
    capRate = 2  # time between captures
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


def buildVideoData(CNNfolder='./'):

    if(DATABASE_DIR[0] == "/" or DATABASE_DIR[0] == "~"):
        print "\n\nDatabase directory is absolute. Ignoring current directory..."
        CNNfolder = ""

    print "Loading data from " + CNNfolder + DATABASE_DIR + VIDEO_FOLDER
    print '\n\nLoading training data...'
    [trainingDir] \
        = glob(CNNfolder + DATABASE_DIR + VIDEO_FOLDER + 'Training')
    trainingLabelDict \
        = createLabelDict(CNNfolder + DATABASE_DIR + LABEL_FOLDER + 'Training/')
    trainingX, trainingY \
        = retrieveDataFrom(trainingDir, trainingLabelDict)
    print(trainingX.shape)
    trainingX = trainingX.reshape(-1, 1, trainingX.shape[1], trainingX.shape[2])


    print '\n\nLoading validation data...'
    [validationDir] \
        = glob(CNNfolder + DATABASE_DIR + VIDEO_FOLDER + 'Development')
    validationLabelDict \
        = createLabelDict(CNNfolder + DATABASE_DIR + LABEL_FOLDER + 'Development/')
    validationX, validationY \
        = retrieveDataFrom(validationDir, validationLabelDict)
    print(validationX.shape)
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

def loadSingleVideo(videoPath, locks, images, labels, directory, labelsDict):
    (imageLock, labelLock) = locks
    filename = videoPath.split('/')[-1][:-4]  # e.g. 203_1_Northwind_video
    patientNum = filename[:5]  # e.g. 203_1
    # print patientNum, 'has label', labelsDict[patientNum]
    picklePath = directory + '/pickledData/' + filename + '.save'
    if os.path.exists(picklePath):  # check if it exists first
        print 'Loading pickled data of ' + filename
        curImages = pickle.load(open(picklePath, 'r'))
    else:
        print 'Extracting data for ' + filename
        rawImages = extractImagesfromVideo(videoPath)
        print 'Normalising ' + filename
        rawImages = 1 - (rawImages/255.0)
        print 'Scaling ' + filename
        curImages = [zoom(image, 0.2) for image in rawImages]
        print 'Pickling data in ' + picklePath
        pickle.dump(curImages, open(picklePath, 'w'))
    imageLabel = labelsDict[patientNum]
    mult = [1, 2, 2, 4]

    with imageLock:
        for x in range(mult[imageLabel]):
            images.extend(curImages)  # add images to list of examples
    with labelLock:
        labels.extend([imageLabel] * len(curImages) * mult[imageLabel])  # assign corresponding label

def loadWorker(queue, locks, images, labels, directory, labelsDict):
    while True:
        if(queue.empty()):
            return
        path = queue.get()
        loadSingleVideo(path, locks, images, labels, directory, labelsDict)
        queue.task_done()


# retrieve videos from subdirectories within current directory
def retrieveDataFrom(directory, labelsDict):
    rawVideoPaths = ([ glob(x + '/*') for x in glob(directory + '/[!p]*') ])
    if not os.path.exists(directory + '/pickledData/'):
        os.mkdir(directory + '/pickledData/')  # pickle dir doesn't exist so make it
    queue = Queue()
    for folder in rawVideoPaths:
        for path in folder:
            queue.put(path)
    images = []
    labels = []
    imageLock = threading.Lock()
    labelLock = threading.Lock()
    for i in range(4):
        t = threading.Thread(target=loadWorker, args=(queue, (imageLock, labelLock), images, labels, directory, labelsDict))
        t.daemon = True
        t.start()

    queue.join()

    numExamples = len(images)
    order = np.random.permutation(numExamples)
    newImages = [images[x] for x in order]
    newLabels = [labels[x] for x in order]

    return (np.array(newImages, dtype='float32')), np.array(newLabels, dtype='int32')


# takes an path to the video file and a network and returns an array containing
# the number of times it predicted each label for the different images
def predictVideo(videoFilePath, network):
    # extract the images
    rawImages = extractImagesfromVideo(videoFilePath)
    rawImages = 1 - (rawImages/255.0)
    curImages = np.array([zoom(image, 0.2) for image in rawImages], dtype='float32')
    curImages = curImages.reshape(-1, 1, curImages.shape[1], curImages.shape[2])
    # predict using the network
    predictions = network.predict(curImages)

    return dict(Counter(predictions))

def main():
    print "Loading net.."
    network = loadNet('../videoCNN1.save')
    print "Predicting.."
    print predictVideo('../205_1_Freeform_video.mp4', network)

if __name__ == '__main__':
    main()
