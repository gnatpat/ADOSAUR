import pickle
from testEnums import *  # filepaths for testing material
from ..utils import VideoUtils as VU


##################$#
# VIDEOUTILS TESTS #
###################$

def testRgbExtractsAnObject():
    actOutput = VU.extractRGB(TEST_PICTURE_PATH)
    assert actOutput != None

def testRgbExtractsCorrectImage():
    actOutput = VU.extractRGB(TEST_PICTURE_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_PICTURE_PATH, 'r'))
    assert (actOutput == expOutput).all()

def testGrayscaleExtractsAnObject():
    actOutput = VU.extractGrayScale(TEST_PICTURE_PATH)
    assert actOutput != None

def testImagesfromVideoExtractsAnObject():
    actOutput = VU.extractImagesfromVideo(TEST_PICTURE_PATH)
    assert actOutput != None

def testImagesfromVideoExtractsGrayscaleImage():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH, grayscale=True)
    expOutput = pickle.load(open(TEST_PICKLED_GRAYSCALE_VIDEO_PATH))
    assert (actOutput == expOutput).all()

def testImagesfromVideoExtractsHasGrayscaleImageDefault():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_GRAYSCALE_VIDEO_PATH,'r'))
    assert (actOutput == expOutput).all()

def testImagesfromVideoExtractsRgbImage():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH, grayscale=False)
    expOutput = pickle.load(open(TEST_PICKLED_RGB_VIDEO_PATH))
    assert (actOutput == expOutput).all()

# Excluded: need 700mb pickled network
# def testPredictVideo():
#     pass

# Excluded: writes 3GB of data and takes about 5 minutes
# def testBuildVideoDataReturnsObjects():
#     trainingX, trainingY, validationX, validationY, testingX, testingY = VU.buildVideoData('cnn/')
#     assert trainingX == None
#     assert trainingY == None
#     assert validationX == None
#     assert validationY == None
#     assert testingX == None
#     assert testingY == None
