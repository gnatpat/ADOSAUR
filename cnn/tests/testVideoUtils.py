import pickle
from testEnums import *  # filepaths for testing material
from ..utils import VideoUtils as VU


##################$#
# VIDEOUTILS TESTS #
###################$

def testExtractRgbExtactsAnObject():
    actOutput = VU.extractRGB(TEST_PICTURE_PATH)
    assert actOutput != None

def testExtractRgbExtactsCorrectImage():
    actOutput = VU.extractRGB(TEST_PICTURE_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_PICTURE_PATH, 'r'))
    assert actOutput == expOutput

# TODO: fix test image
def testExtractGrayscaleExtactsAnObject():
    actOutput = VU.extractGrayScale(TEST_PICTURE_PATH)
    assert actOutput != None

# TODO: fix test image
def testExtractGrayscaleExtactsCorrectImage():
    actOutput = VU.extractGrayScale(TEST_PICTURE_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_PICTURE_PATH, 'r'))
    assert actOutput == expOutput

def testExtractImagesfromVideoExtractsAnObject():
    actOutput = VU.extractImagesfromVideo(TEST_PICTURE_PATH)
    assert actOutput != None

def testExtractImagesfromVideoExtractsGrayscaleImage():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH, grayscale=True)
    expOutput = pickle.load(open(TEST_PICKLED_GRAYSCALE_VIDEO_PATH))
    assert actOutput == expOutput

def testExtractImagesfromVideoExtractsHasGrayscaleImageDefault():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_GRAYSCALE_VIDEO_PATH,'r'))
    assert actOutput == expOutput

def testExtractImagesfromVideoExtractsRgbImage():
    actOutput = VU.extractImagesfromVideo(TEST_VIDEO_PATH, grayscale=False)
    expOutput = pickle.load(open(TEST_PICKLED_RGB_VIDEO_PATH))
    assert actOutput == expOutput

def testPredictVideo():
    pass  # need to build a network -- come back

def testRetrieveDataFrom():
    pass  # need data

def testBuildVideoData():
    pass # need data
